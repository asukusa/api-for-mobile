import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch

from ..main import app
from ..users.models import User
from .schemas import ReactionIn, ReactionCreate, Reaction
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
async def test_create_reaction():
    reaction_data = {"type": "like", "to_user_id": 2}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/", json=reaction_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["type"] == "like"

@pytest.mark.asyncio
async def test_get_gotten_reactions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/gotten/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_posted_reactions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/posted/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
