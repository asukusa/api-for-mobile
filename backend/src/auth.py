from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select, Result, Row
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from passlib.hash import bcrypt_sha256

from .users import User
from src.config import settings
from .database import db_manager


class UserAuth(BaseModel):
    username: str
    password: str


def get_password_hash(password: str) -> str:
    return bcrypt_sha256.hash(password, salt=settings.salt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password


async def authenticate_dependency(
    auth_user: UserAuth,
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> Row[User]:
    username = auth_user.username
    password = auth_user.password
    query = select(User).filter(User.username == username)
    result: Result = await session.execute(query)
    user = result.scalars().first()

    if user is not None and verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Неверный логин или пароль",
    )
