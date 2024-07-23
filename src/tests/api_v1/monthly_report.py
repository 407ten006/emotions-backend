from datetime import datetime, timedelta

import pytest
from core.config import settings
from httpx import AsyncClient
from models import User, Diary, MonthlyReport
from models.auth import AuthToken
from models.diaries import DiaryCreate
import pytest
from core.config import settings
from httpx import AsyncClient
from models import User
from models.auth import AuthToken
from models.diaries import Diary, DiaryCreate
from sqlmodel import Session

from models.emotion_reacts import EmotionReactCreate, EmotionReact
from models.monthly_report import MonthlyReportCreate
from utils.utils import get_kst_today_yymmdd

pytestmark = pytest.mark.asyncio


async def test_create_monthly_report_감정_리포트_생성(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    created_date_yymm = get_kst_today_yymmdd()[:6]
    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="그저께 일기",
            created_datetime=datetime.now()-timedelta(days=3),
            chosen_emotion_id = 1
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="어제 일기",
            created_datetime=datetime.now() - timedelta(days=2),
            chosen_emotion_id=1
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘 일기",
            created_datetime=datetime.now() - timedelta(days=1),
            chosen_emotion_id=2
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)



    response = await async_client.post(
        f"{settings.API_V1_STR}/monthly_report/",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
        json={
            "created_date_yymm": created_date_yymm,
        }
    )


    print(response.json())


async def test_get_monthly_report(
        async_client: AsyncClient,
        sample_user: User,
        login_sample_user: AuthToken,
        db_session: Session,
):
    created_date_yymm = get_kst_today_yymmdd()[:6]
    monthly_report_create = MonthlyReportCreate(
        user_id=sample_user.id,
        created_date_yymm=created_date_yymm,
        content="monthly report test"
    )

    monthly_report = MonthlyReport.from_orm(monthly_report_create)

    db_session.add(monthly_report)
    db_session.commit()
    db_session.refresh(monthly_report)


    response = await async_client.post(
        f"{settings.API_V1_STR}/monthly_report/{created_date_yymm}",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )

    print(response.json())