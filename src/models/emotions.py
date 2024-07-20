from datetime import datetime

from sqlmodel import Field,SQLModel
from typing import Optional
from src.utils.utils import utc_now


class Emotion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    diary_id: int = Field(foreign_key="diary.id", index=True)
    emotion: str
    content: str
    created_date: datetime = Field(default_factory=utc_now)
    percent: Optional[float]=Field(default=None)

