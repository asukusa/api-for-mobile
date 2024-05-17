import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

from ..main import app
from .models import User
from .schemas import UserCreate
from ..auth import authenticate_dependency
from ..database import db_manager


# Имитация зависимостей
async def override_authenticate_dependency():
    return User(id=1, username="testuser")


async def override_db_session_dependency() -> AsyncSession:
    return AsyncMock(spec=AsyncSession)


app.dependency_overrides[authenticate_dependency] = override_authenticate_dependency
app.dependency_overrides[db_manager.session_dependency] = override_db_session_dependency


@pytest.mark.asyncio
@patch("app.service.get_users", new_callable=AsyncMock)
async def test_get_users(mock_get_users):
    mock_get_users.return_value = [User(id=1, username="testuser")]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()[0]["username"] == "testuser"
    mock_get_users.assert_called_once()


@pytest.mark.asyncio
@patch("app.service.create_user", new_callable=AsyncMock)
async def test_create_user(mock_create_user):
    user_data = {"username": "newuser", "password": "newpassword"}
    mock_create_user.return_value = User(id=2, username="newuser")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "newuser"
    mock_create_user.assert_called_once()


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"
