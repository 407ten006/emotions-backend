from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from src.models import Diary
from src.utils.utils import utc_now


class EmotionReactBase(SQLModel):
    diary_id: int = Field(foreign_key="diary.id", index=True)
    emotion_id: int = Field(foreign_key="emotion.id")
    content: str = Field(..., max_length=100)
    percent: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    created_datetime: datetime


class EmotionReactCreate(SQLModel):
    diary_id: int
    emotion_id: int
    content: str = Field(..., max_length=100)
    percent: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    created_datetime: datetime = Field(default_factory=utc_now)


class EmotionReact(EmotionReactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    diary: "Diary" = Relationship(back_populates="emotion_reacts")


class EmotionReactPublic(EmotionReactBase):
    id: int
    created_date_yymmdd: str


class EmotionReactsPublic(SQLModel):
    data: list[EmotionReactPublic]
    count: int
