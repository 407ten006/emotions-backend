from typing import Any

from fastapi import APIRouter, Query, Request, HTTPException
from typing import Any
from src.api.v1.deps import CurrentUser

router = APIRouter()


@router.get("/today")
def get_today_diary(current_user: CurrentUser) -> Any:
    """
    오늘의 다이어리 조회

    이미 다이어리 작성했다면, 해당 다이어리 조회, 추가 수정 불가
    """
    return current_user


@router.get("/")
def get_diaries(current_user: CurrentUser, month: int = Query(), date_type: str = Query()) -> Any:
    """
    월별 다이어리 조회
    """

    return current_user


@router.post("/")
def create_diary(request: Request,current_user: CurrentUser) -> Any:

    try:
        body = request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    content = body.get("content")

    print(f"Diary content: {content}")
    """
    다이어리 생성 & 분석
    """



    return {}


@router.get("/{diary_id}")
def get_diary(current_user: CurrentUser, diary_id: int) -> Any:
    """
    다이어리 상세 조회

    """
    return current_user


@router.patch("/{diary_id}")
def update_diary(current_user: CurrentUser, main_emotion: str = Query(None)) -> Any:
    """
    오늘의 메인 감정 선택
    """
    return {}


@router.get("/monthly-report")
def get_monthly_report(current_user: CurrentUser, month: int) -> Any:
    """
    월간 감정 분석
    """
    return {}


@router.post("/clova-test")
def clova_test(memo: str) -> Any:
    """
    클로바 테스트

    """
    # 클로바 API 분석
    return {'result': ""}
