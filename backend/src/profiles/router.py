from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..users import User
from ..auth import authenticate_dependency
from . import service
from .schemas import (
    Profile,
    ProfileCreate,
    ProfileUpdatePartial,
    ProfileIn,
    ProfilePhotoVerification,
)
from ..database import db_manager


router = APIRouter(tags=["Profiles"])


@router.get(
    "/",
    response_model=List[Profile],
    description="**Don't use for mobile!** It's just for monitoring",
)
async def get_all_profiles(
    session: AsyncSession = Depends(db_manager.session_dependency),
):
    return await service.get_profiles(session=session)


@router.post(
    "/",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
    description="Create new profile",
)
async def create_profile(
    profile: ProfileIn,
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    profile = ProfileCreate(user_id=auth_user.id, **profile.model_dump())
    return await service.create_profile(session=session, profile_in=profile)


@router.post("/own/", response_model=Profile, description="Get own profile")
async def get_own_profile(
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    return await service.get_profile_by_username(
        session=session, username=auth_user.username
    )


@router.post(
    "/selection/",
    response_model=List[Profile],
    description="Get a list of recommended profiles",
)
async def get_profiles(
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    return await service.get_profiles(session=session)


@router.post(
    "/verify_photo/", response_model=bool, description="Verify profile photo"
)
async def verify_photo(
    photo: ProfilePhotoVerification,
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    return await service.verify_profile(
        photo=photo, session=session, auth_user=auth_user
    )


@router.patch(
    "/",
    response_model=Profile,
    description="Update profile information. Don't require all profile attributes",
)
async def update_partial_profile(
    profile: ProfileUpdatePartial,
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    profile_bd = await service.get_profile_by_username(
        username=auth_user.username, session=session
    )
    return await service.update_profile(
        session=session,
        profile=profile_bd,
        profile_update=profile,
        partial=True,
    )


# @router.put("/{profile_id}")
# async def update_profile(
#     profile_update: ProfileUpdate,
#     profile: Profile = Depends(profile_by_id_dependency),
#     session: AsyncSession = Depends(db_manager.session_dependency),
# ):
#     return await service.update_profile(
#         session=session, profile=profile, profile_update=profile_update
#     )


# @router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_profile(
#     profile: Profile = Depends(profile_by_id_dependency),
#     session: AsyncSession = Depends(db_manager.session_dependency),
# ):
#     await service.delete_profile(session=session, profile=profile)

# @router.get("/{profile_id}", response_model=Profile)
# async def get_profile_by_id(
#     profile: Profile = Depends(profile_by_id_dependency),
# ):
#     return profile
