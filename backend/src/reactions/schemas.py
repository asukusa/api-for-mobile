from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ReactionsEnum(str, Enum):
    like = "like"
    dislike = "dislike"


class ReactionBase(BaseModel):
    to_user_id: int
    type: ReactionsEnum


class ReactionIn(ReactionBase):
    pass


class ReactionCreate(ReactionBase):
    from_user_id: int


class Reaction(ReactionBase):
    id: int
    from_user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
