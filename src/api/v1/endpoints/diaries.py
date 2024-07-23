from http import HTTPStatus
from typing import Any

from api.v1.deps import CurrentUser, SessionDep
from api.v1.global_response import create_response
from core.clova_model_api import CompletionExecutor
from core.enums import EmotionEnum
from cruds import diaries as diaries_cruds
from cruds import emotions as emotions_crud
from cruds import emotions_reacts as emotions_reacts_cruds
from fastapi import APIRouter, Body, HTTPException, Path, Query
from models.diaries import (
    DiariesMonth,
    DiaryCreate,
    DiaryCreateRequest,
    DiaryMonth,
    DiaryPublic,
    TodayDiaryPublic,
)
from models.emotion_reacts import EmotionReactCreate
from starlette import status
from utils.utils import get_kst_today_yymmdd

router = APIRouter()


@router.get("/today", status_code=status.HTTP_200_OK, response_model=TodayDiaryPublic)
async def get_today_diary(session: SessionDep, current_user: CurrentUser):
    """
    오늘의 다이어리 조회, 한국 시간 기준

    이미 다이어리를 작성했다면, 해당 다이어리 조회, 추가 수정 불가
    """

    kst_today_yymmdd = get_kst_today_yymmdd()
    today_diary = await diaries_cruds.get_today_diary(
        session=session,
        user_id=current_user.id,
        kst_search_date_yymmdd=kst_today_yymmdd,
    )

    # print(today_diary)
    emotions = []
    if today_diary:
        emotions = [
            emotion_react.emotion for emotion_react in today_diary.emotion_reacts
        ]
        response = {
            "can_create": True,
            "diary": DiaryPublic.from_orm(today_diary).dict(),
        }
        print(response)
        return create_response(True, "", response, HTTPStatus.OK)

    else:
        return create_response(False,"Error",None,HTTPStatus.NOT_FOUND)



@router.get("/", status_code=status.HTTP_200_OK,response_model=DiariesMonth)
async def get_diaries(session: SessionDep, current_user: CurrentUser, search_date_yymm: str = Query()):
    """
    월별 다이어리 조회
    """


    if not search_date_yymm:
        return create_response(False,"Error",None,HTTPStatus.NOT_FOUND)


    diaries = await diaries_cruds.get_diaries_by_month(
        session = session,
        user_id=current_user.id,
        search_date_yymm=search_date_yymm,
    )
    response_data = DiariesMonth(
        diaries=[DiaryMonth.from_orm(diary).dict() for diary in diaries]
    )
    return create_response(True,"",response_data.dict(),HTTPStatus.OK)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DiaryPublic)
async def create_diary(
    current_user: CurrentUser,
    session: SessionDep,
    diary_create_req: DiaryCreateRequest = Body(...),
):
    """
    1. Model API 호출
    2. API가 올바를 경우 값을 Emotions과 Diary를 DB에 넣기
    3. 만들어진 Map 2개를 Return
    """

    user_input = diary_create_req.content
    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6",
        api_key_primary_val="K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q",
        request_id="b109906c-e945-4c19-9d30-8bd62bd8f0a7",
    )

    response_data = completion_executor.execute(user_input)

    if response_data is None:
        return create_response(False,"Error",None,HTTPStatus.BAD_REQUEST)

    emotions = response_data.get("emotions")
    percentage = response_data.get("percentage")

    new_diary = DiaryCreate(user_id=current_user.id, content=user_input)

    created_diary = await diaries_cruds.create_diary(
        session=session, diary_create=new_diary
    )

    for emotion_enum in EmotionEnum:
        if emotion_enum.name in emotions and emotion_enum.name in percentage:
            emotion = await emotions_crud.get_emotion_by_name(session=session, name=emotion_enum.name)
            new_emotion_react = EmotionReactCreate(
                diary_id=created_diary.id,
                emotion_id=emotion.id,
                content=emotions[emotion_enum.name],
                percent=percentage[emotion_enum.name],
            )

            await emotions_reacts_cruds.create_emotion_react(
                session=session, emotion_react_create=new_emotion_react
            )

    return create_response(True,"",created_diary.dict(),HTTPStatus.CREATED)


@router.get("/{diary_id}", status_code=status.HTTP_200_OK, response_model=DiaryPublic)
async def get_diary(session: SessionDep, current_user: CurrentUser, diary_id: int):
    """
    다이어리 상세 조회
    """

    diary = await diaries_cruds.get_diary_by_id(session=session, diary_id=diary_id)

    print(diary)
    if diary is None:
        return create_response(False,"Error",None,HTTPStatus.NOT_FOUND)

    return create_response(True,"",diary.dict(),HTTPStatus.OK)


@router.patch("/{diary_id}", status_code=status.HTTP_200_OK, response_model=DiaryPublic)
async def update_diary(
    session: SessionDep, current_user: CurrentUser, diary_id:int = Path(), main_emotion_id: int = Body(...)
) -> Any:
    """
    오늘의 메인 감정 선택
    1. id 값으로 다이어리 조히
    2. Diary의 choosen값을 고른 값으로 설정
    """

    diary = await diaries_cruds.get_diary_by_id(session=session, diary_id=diary_id)
    # TODO: 리액션이 없는 감정 선택 시, 예외 처리
    await diaries_cruds.update_main_emotion(session=session, diary=diary, emotion_id=main_emotion_id)

    return diary


@router.get("/monthly-report", status_code=status.HTTP_200_OK)
async def get_monthly_report(current_user: CurrentUser, month: int) -> Any:

    """
    월간 감정 분석
    """

    return {}
