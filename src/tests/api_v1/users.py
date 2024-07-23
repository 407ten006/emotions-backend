import pytest
from core.config import settings
from httpx import AsyncClient
from models import User
from models.auth import AuthToken
from models.diaries import Diary, DiaryCreate
from sqlmodel import Session

from models.emotion_reacts import EmotionReactCreate, EmotionReact
from utils.utils import get_kst_today_yymmdd

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_me_내정보_조회(
        async_client: AsyncClient,
        sample_user: User,
        login_sample_user: AuthToken
):
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/me",  # URL이 /me로 설정된 경우
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"}
    )

    response_data = response.json()
    print(response_data)

async def test_update_me_내정보_업데이트(
        async_client: AsyncClient,
        sample_user: User,
        login_sample_user: AuthToken
):
    response = await async_client.patch(
        f"{settings.API_V1_STR}/users/me",  # URL이 /me로 설정된 경우
        headers={"Authorization": f"Bearer {login_sample_user.access_token}"}
    )

    response_data = response.json()
    print(response_data)
