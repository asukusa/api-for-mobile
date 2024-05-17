from typing import List

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.exceptions import HTTPException

from ..ml.photo_verification import photo_verification
from ..users import User
from .models import Profile
from .schemas import (
    ProfileCreate,
    ProfileUpdate,
    ProfileUpdatePartial,
    ProfilePhotoVerification,
)


async def get_profiles(session: AsyncSession) -> List[Profile]:
    stmt = select(Profile).order_by(Profile.id)
    result: Result = await session.execute(stmt)
    profiles = result.scalars().all()
    return list(profiles)


async def get_profile_by_id(
    session: AsyncSession, profile_id: int
) -> Profile | None:
    return await session.get(Profile, profile_id)


async def get_profile_by_username(
    session: AsyncSession, username: str
) -> Profile:
    query = (
        select(User)
        .options(joinedload(User.profile))
        .filter(User.username == username)
    )
    result = await session.execute(query)
    user = result.scalars().first()
    profile = user.profile
    if profile is None:
        raise HTTPException(detail="Профиль не найден", status_code=status.HTTP_404_NOT_FOUND)
    return profile


async def create_profile(
    session: AsyncSession, profile_in: ProfileCreate
) -> Profile:
    profile = Profile(**profile_in.model_dump())
    session.add(profile)
    await session.commit()
    # await session.refresh()
    return profile


async def update_profile(
    session: AsyncSession,
    profile: Profile,
    profile_update: ProfileUpdate | ProfileUpdatePartial,
    partial: bool = False,
) -> Profile:
    for name, value in profile_update.model_dump(
        exclude_unset=partial
    ).items():
        setattr(profile, name, value)
    await session.commit()
    return profile


async def delete_profile(session: AsyncSession, profile: Profile) -> None:
    await session.delete(profile)
    await session.commit()


async def verify_profile(
    session: AsyncSession, auth_user: User, photo: ProfilePhotoVerification
) -> bool:
    profile = await get_profile_by_username(
        username=auth_user.username, session=session
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден"
        )
    is_verified = await photo_verification(
        profile_photo_base64=profile.photo_base64,
        photo_in_base64=photo.photo_base64,
    )
    profile.is_verified = is_verified
    await session.commit()

    return is_verified
