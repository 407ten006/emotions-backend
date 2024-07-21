from typing import Any

from fastapi import APIRouter, Query

from src.api.v1.deps import CurrentUser, SessionDep
from src.cruds import diaries as diaries_cruds
from src.models.diaries import DiaryPublic
from src.utils.utils import kst_today_yymmdd

router = APIRouter()


@router.get("/today")
def get_today_diary(
    session: SessionDep, current_user: CurrentUser
) -> DiaryPublic | None:
    """
    오늘의 다이어리 조회

    이미 다이어리 작성했다면, 해당 다이어리 조회, 추가 수정 불가
    """

    today_yymmdd = kst_today_yymmdd()
    today_diary = diaries_cruds.get_today_diary(
        session=session, user_id=current_user.id, search_date_yymmdd=today_yymmdd
    )

    return today_diary


@router.get("/")
def get_diaries(
    current_user: CurrentUser, search_date_yymm: str = Query()
) -> Any:
    """
    월별 다이어리 조회
    """
    return {}


@router.post("/")
def create_diary(current_user: CurrentUser) -> Any:
    """

    1. Model API 호출
    2. API가 올바를 경우 값을 Emotions과 Diary를 DB에 넣기
    3. 만들어진 Map 2개를 Return
    """

    return {}


@router.get("/{diary_id}")
def get_diary(current_user: CurrentUser, diary_id: int) -> Any:
    """
    다이어리 상세 조회

    1. id 값으로 다이어리를 조회
    2. Emotion을 순회하면서 id값에 해당하는 것들을 전부 가져오기
    3. 1+2 의 결과를 합쳐서 보여주기
    """
    return current_user


@router.patch("/{diary_id}")
def update_diary(current_user: CurrentUser, main_emotion: str = Query(None)) -> Any:
    """
    오늘의 메인 감정 선택
    1. id 값으로 다이어리 조히
    2. Diary의 choosen값을 고른 값으로 설정
    """
    return {}


@router.get("/monthly-report")
def get_monthly_report(current_user: CurrentUser, month: int) -> Any:
    """
    월간 감정 분석
    """
    return {}
