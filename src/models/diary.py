from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from src.utils.utils import utc_now


class Diary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(...)
    chosen_emotion: Optional[int] = Field(...)
    created_date: datetime = Field(default_factory=utc_now)
