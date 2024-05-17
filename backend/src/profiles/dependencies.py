from typing import Annotated

from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from . import service
from .models import Profile
from ..database import db_manager


async def profile_by_id_dependency(
    profile_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> Profile:
    profile = await service.get_profile_by_id(
        session=session, profile_id=profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Профиль с ID: {profile_id} не найден",
        )
    return profile


async def profile_by_username_dependency(
    username: Annotated[str, Path],
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> Profile:
    profile = await service.get_profile_by_username(
        session=session, username=username
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Профиль с username: {username} не найден",
        )
    return profile
