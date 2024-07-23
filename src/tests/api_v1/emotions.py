import pytest
from core.config import settings
from httpx import AsyncClient
from models import User
from models.auth import AuthToken
from models.diaries import Diary, DiaryCreate
from sqlmodel import Session
from models.emotion_reacts import EmotionReact, EmotionReactCreate
from utils.utils import get_kst_today_yymmdd

pytestmark = pytest.mark.asyncio


async def test_get_emotions_감정이들_전체_조회(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    diary = Diary.from_orm(
        DiaryCreate(
            user_id=sample_user.id,
            content="오늘의 일기",
        )
    )

    db_session.add(diary)
    db_session.commit()
    db_session.refresh(diary)

    emotion_react_create = EmotionReactCreate(
        diary_id=diary.id, emotion_id=1, content="정말 기뻐요!", percent=80
    )

    emotion_react = EmotionReact.from_orm(emotion_react_create)
    db_session.add(emotion_react)
    db_session.commit()
    db_session.refresh(emotion_react)

    response = await async_client.get(
        f"{settings.API_V1_STR}/emotion_reacts",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )

    print(response.json())
