import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

from ..main import app
from .models import Profile
from ..users.models import User
from .schemas import ProfileIn, ProfileUpdatePartial, ProfilePhotoVerification
from ..auth import authenticate_dependency
from ..database import db_manager


async def override_authenticate_dependency():
    return User(id=1, username="testuser")

async def override_db_session_dependency() -> AsyncSession:
    return AsyncMock(spec=AsyncSession)

app.dependency_overrides[authenticate_dependency] = override_authenticate_dependency
app.dependency_overrides[db_manager.session_dependency] = override_db_session_dependency

@pytest.mark.asyncio
async def test_get_profiles():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/selection/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_profile():
    profile_data = {"name": "Test", "age": 30}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/", json=profile_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test"

@pytest.mark.asyncio
async def test_update_partial_profile():
    profile_update_data = {"age": 31}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch("/", json=profile_update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["age"] == 31

@pytest.mark.asyncio
async def test_verify_photo():
    photo_data = {"photo_url": "http://example.com/photo.jpg"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/verify_photo/", json=photo_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
