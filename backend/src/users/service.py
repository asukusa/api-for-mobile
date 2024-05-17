from typing import List

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.exceptions import HTTPException

from ..auth import get_password_hash
from .models import User
from .schemas import UserCreate


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession, user_in: UserCreate
) -> User | None:
    hash_password = get_password_hash(user_in.password)
    user = User(
        username=user_in.username,
        hashed_password=hash_password,
    )
    session.add(user)
    try:
        await session.commit()
        # await session.refresh()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с данным username уже существует",
        )
    return user
