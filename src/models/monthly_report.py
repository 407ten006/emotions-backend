from datetime import datetime

from sqlmodel import Field, SQLModel
from utils.utils import utc_now


class MonthlyReportBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", index=True)
    created_date_yymm: str = Field(..., max_length=4)
    content: str = Field(..., max_length=1000)
    created_datetime: datetime


class MonthlyReportCreate(SQLModel):
    user_id: int
    created_date_yymm: str = Field(..., max_length=4)
    content: str = Field(..., max_length=1000)
    created_datetime: datetime = Field(default_factory=utc_now)


class MonthlyReport(MonthlyReportBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MonthlyReportPublic(MonthlyReportBase):
    id: int
    created_date_yymmdd: str
