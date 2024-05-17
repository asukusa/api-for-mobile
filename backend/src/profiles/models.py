from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from ..database import Base


class Profile(Base):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(nullable=False)
    sex: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    hobbies: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    photo_base64: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    @declared_attr
    def user(cls):
        return relationship(
            "User", back_populates="profile", single_parent=True
        )
