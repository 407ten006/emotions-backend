import pytest
from httpx import AsyncClient
from sqlmodel import Session

from core.config import settings
from models import User
from models.auth import AuthToken
from models.diaries import Diary, DiaryCreate

pytestmark = pytest.mark.asyncio


async def test__get_today_diary__오늘_기록이_없는_경우(
    async_client: AsyncClient, sample_user: User, login_sample_user: AuthToken
):
    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/today",
        headers={"Authorization": f"{login_sample_user.access_token}"},
    )

    assert response.status_code == 200
    assert response.json() == None


async def test__get_today_diary__오늘_기록이_있는_경우(
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

    response = await async_client.get(
        f"{settings.API_V1_STR}/diaries/today",
        headers={"Authorization": f"{login_sample_user.access_token}"},
    )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == diary.id
    assert response_json["content"] == diary.content
    assert response_json["created_datetime"] == diary.created_datetime.isoformat()
    assert response_json["chosen_emotion_id"] is None
    assert response_json["user_id"] == sample_user.id


async def test_create_diary_api(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    user_input = "안녕하세요!"

    response = await async_client.post(
        f"{settings.API_V1_STR}/diaries",
        headers={"Authorization": f"{login_sample_user.access_token}"},
        json={"content": user_input},
    )

    print(response)