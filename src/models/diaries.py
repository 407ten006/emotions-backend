from datetime import datetime
from typing import TYPE_CHECKING

from models.emotion_reacts import EmotionReactPublic
from sqlmodel import Field, Relationship, SQLModel
from utils.utils import utc_now

if TYPE_CHECKING:
    from models import EmotionReact


class DiaryBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", index=True)
    content: str = Field(..., max_length=300)
    chosen_emotion_id: int | None = Field(default=None)
    created_datetime: datetime


class DiaryCreate(SQLModel):
    user_id: int
    content: str = Field(..., max_length=300)
    created_datetime: datetime = Field(default_factory=utc_now)


class DiaryCreateRequest(SQLModel):
    content: str = Field(..., max_length=300)


class DiaryUpdate(SQLModel):
    main_emotion_id: int


class Diary(DiaryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    emotion_reacts: list["EmotionReact"] = Relationship(back_populates="diary")


class DiaryPublic(SQLModel):
    id: int
    content: str
    chosen_emotion_id: int | None
    emotion_reacts: list[EmotionReactPublic]


class DiaryMonth(SQLModel):
    id: int
    chosen_emotion_id: int | None = None
    created_datetime: datetime = Field(default_factory=utc_now)


class DiariesMonth(SQLModel):
    diaries: list[DiaryMonth]


class DiariesPublic(SQLModel):
    data: list[DiaryPublic]
    count: int


class TodayDiaryPublic(SQLModel):
    can_create: bool
    diary: DiaryPublic | None
    # emotions: list[EmotionPublic]
