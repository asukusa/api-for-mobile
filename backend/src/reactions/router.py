from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import service
from ..auth import authenticate_dependency
from ..users import User
from ..database import db_manager
from .schemas import Reaction, ReactionCreate, ReactionIn


router = APIRouter(tags=["Reactions"])


@router.post(
    "/",
    response_model=Reaction,
    description="Create some reaction (like or dislike)",
)
async def create_reaction(
    reaction: ReactionIn,
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):
    from_user_id = auth_user.id
    reaction = ReactionCreate(
        **reaction.model_dump(), from_user_id=from_user_id
    )
    return await service.create_reactions(session=session, reaction=reaction)


@router.post(
    "/gotten/",
    response_model=List[Reaction],
    description="Get gotten reactions (likes and dislikes)",
)
async def get_gotten_reactions(
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):

    return await service.get_gotten_reactions(session=session, user=auth_user)


@router.post(
    "/posted/",
    response_model=List[Reaction],
    description="Get posted reactions (likes and dislikes)",
)
async def get_posted_reactions(
    session: AsyncSession = Depends(db_manager.session_dependency),
    auth_user: User = Depends(authenticate_dependency),
):

    return await service.get_posted_reactions(session=session, user=auth_user)
