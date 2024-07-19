from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from src.utils.utils import utc_now


class SocialProvider(Enum):
    naver = "naver"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    is_active: bool = Field(default=True)
    service_policy_agreement: bool = Field(default=False)
    privacy_policy_agreement: bool = Field(default=False)
    third_party_information_agreement: bool = Field(default=False)
    nickname: str | None = Field(default=None, max_length=20)
    social_provider: SocialProvider = Field(default=SocialProvider.naver)
    joined_datetime: datetime = Field(default_factory=utc_now)


#
class UserCreate(UserBase):
    social_provider: SocialProvider = Field(default=SocialProvider.naver)
    joined_datetime: datetime = Field(default_factory=utc_now)


class UserUpdateMe(SQLModel):
    nickname: str | None = Field(default=None, max_length=20)
    service_policy_agreement: bool | None = Field(default=None)
    privacy_policy_agreement: bool | None = Field(default=None)
    third_party_information_agreement: bool | None = Field(default=None)
    updated_datetime: datetime = Field(default_factory=utc_now)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
