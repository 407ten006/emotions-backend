from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from utils.utils import utc_now

if TYPE_CHECKING:
    from models import Diary


class EmotionReactBase(SQLModel):
    diary_id: int = Field(foreign_key="diary.id", index=True)
    emotion_id: int
    content: str = Field(..., max_length=300)
    percent: int
    created_datetime: datetime


class EmotionReactCreate(SQLModel):
    diary_id: int
    emotion_id: int
    content: str = Field(..., max_length=300)
    percent: int
    created_datetime: datetime = Field(default_factory=utc_now)


class EmotionReact(EmotionReactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    diary: "Diary" = Relationship(back_populates="emotion_reacts")


class EmotionReactPublic(EmotionReactBase):
    id: int


class EmotionReactsPublic(SQLModel):
    data: list[EmotionReactPublic]
    count: int
