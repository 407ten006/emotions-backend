import json
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Query, Request, HTTPException

from api.v1.deps import CurrentUser, SessionDep
from core.clova_model_api import CompletionExecutor
from cruds import diaries as diaries_cruds
from models.diaries import DiaryPublic,DiaryCreate
from models.emotion_reacts import EmotionReactCreate
from utils.utils import kst_today_yymmdd
from cruds import emotions_reacts as emotions_reacts_cruds
from core.enums import EmotionEnum

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
def get_diaries(current_user: CurrentUser, search_date_yymm: str = Query()) -> Any:
    """
    월별 다이어리 조회
    """
    return {}


@router.post("/")
async def create_diary(current_user: CurrentUser, session: SessionDep, request: Request) -> Any:
    """
    1. Model API 호출
    2. API가 올바를 경우 값을 Emotions과 Diary를 DB에 넣기
    3. 만들어진 Map 2개를 Return
    """

    try:
        body_bytes = await request.body()
        body = json.loads(body_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    user_input = body.get("content")
    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6",
        api_key_primary_val="K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q",
        request_id="b109906c-e945-4c19-9d30-8bd62bd8f0a7",
    )

    response_data = completion_executor.execute(user_input)

    if response_data is None:
        raise HTTPException(status_code=404, detail="Not Found")
    print(response_data)
    emotions = response_data.get("emotions")
    percentage = response_data.get("percentage")

    print(emotions)
    print(percentage)
    today_yymmdd = kst_today_yymmdd()

    new_diary = DiaryCreate(
        user_id=current_user.id,
        content=user_input,
        created_datetime=today_yymmdd
    )

    created_diary = diaries_cruds.create_diary(
        session=session,
        diary_in=new_diary
    )

    for emotion_enum in EmotionEnum:
        if emotion_enum.name in emotions and emotion_enum.name in percentage:
            print(emotions[emotion_enum.name], percentage[emotion_enum.name])
            new_emotion_react = EmotionReactCreate(
                diary_id=created_diary.id,
                emotion_id=emotion_enum.value,
                content=emotions[emotion_enum.name],
                percent=percentage[emotion_enum.name],
                created_datetime=today_yymmdd
            )
            emotions_reacts_cruds.create_emotion_react(session=session, emotion_react_in=new_emotion_react)

    return {
        "diary": created_diary.dict(),
        "emotions": emotions,
        "percentage": percentage,
    }






    ## 다이어리를 id를 참조값을 가지는 Emotions들을 db에 넣기




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
