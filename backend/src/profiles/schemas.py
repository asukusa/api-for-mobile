from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileBase(BaseModel):
    name: str
    sex: str
    age: int
    city: str
    hobbies: list[str]
    status: str
    photo_base64: Optional[str] = None


class ProfileIn(ProfileBase):
    pass


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileDelete(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileUpdatePartial(ProfileBase):
    name: str | None = None
    sex: str | None = None
    age: int | None = None
    city: str | None = None
    hobbies: list[str] | None = None
    status: str | None = None


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    photo_base64: Optional[str]
    is_verified: bool
    user_id: int


class ProfilePhotoVerification(BaseModel):
    photo_base64: str
