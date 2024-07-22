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
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["can_create"] is True
    assert response_json["diary"] is None
    assert response_json["emotions"] == []


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
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
    )

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["can_create"] is False
    assert response_json["diary"]["content"] == "오늘의 일기"
    assert response_json["diary"]["user_id"] == sample_user.id
    assert response_json["emotions"] == []


async def test_create_diary_api(
    async_client: AsyncClient,
    sample_user: User,
    login_sample_user: AuthToken,
    db_session: Session,
):
    user_input = "오늘은 정말 특별한 날이었다. 오랜만에 친구들과 함께 놀이공원에 갔다. 놀이기구를 타면서 모두가 신나게 웃었고, 햇살도 따뜻하게 우리를 감싸주었다. 그런데 집으로 돌아오는 길에 우산을 잃어버린 것을 알았다. 그래도 친구들과의 추억 덕분에 하루가 행복하게 마무리되었다. !"

    response = await async_client.post(
        f"{settings.API_V1_STR}/diaries/",
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"},
        json={"content": user_input},
    )

    print(response)
