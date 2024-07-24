from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from models import MonthlyReport
from models.diaries import Diary, DiaryCreate
from sqlmodel import Session, select, func


async def get_monthly_report_by_date(
    session: Session, user_id: int, created_date_yymm: str
) -> MonthlyReport:
    statement = (
        select(MonthlyReport)
        .where(MonthlyReport.user_id == user_id)
        .where(MonthlyReport.created_date_yymm == created_date_yymm)
    )

    return session.exec(statement).first()
