from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import declared_attr, relationship, mapped_column, Mapped

from ..database import Base


class Reaction(Base):
    __tablename__ = "reactions"

    type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    from_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @declared_attr
    def from_user(cls):
        return relationship(
            "User",
            foreign_keys=[cls.from_user_id],
            back_populates="posted_reactions",
        )

    @declared_attr
    def to_user(cls):
        return relationship(
            "User",
            foreign_keys=[cls.to_user_id],
            back_populates="gotten_reactions",
        )
