from http import HTTPStatus

from api.v1.deps import CurrentUser, SessionDep
from api.v1.global_response import create_response
from core.clova_model_api import CompletionExecutor
from core.enums import EmotionEnum
from cruds import diaries as diaries_cruds
from cruds import emotions_reacts as emotions_reacts_cruds
from fastapi import APIRouter, Body, Path, Query
from models.diaries import (
    DiariesMonth,
    DiaryCreate,
    DiaryCreateRequest,
    DiaryMonth,
    DiaryPublic,
    DiaryUpdate,
    TodayDiaryPublic,
)
from models.emotion_reacts import EmotionReactCreate, EmotionReactPublic
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

    if today_diary:
        response = {
            "can_create": True,
            "diary": DiaryPublic.from_orm(today_diary).dict(),
        }
        return create_response(True, "", response, HTTPStatus.OK)

    else:
        return create_response(False, "Error", None, HTTPStatus.NOT_FOUND)


@router.get("/", status_code=status.HTTP_200_OK, response_model=DiariesMonth)
async def get_diaries(
    session: SessionDep, current_user: CurrentUser, search_date_yymm: str = Query()
):
    """
    월별 다이어리 조회
    """

    if not search_date_yymm:
        return create_response(False, "Error", None, HTTPStatus.NOT_FOUND)

    diaries = await diaries_cruds.get_diaries_by_month(
        session=session,
        user_id=current_user.id,
        search_date_yymm=search_date_yymm,
    )
    response_data = DiariesMonth(
        diaries=[DiaryMonth.from_orm(diary) for diary in diaries]
    )
    return create_response(True, "", response_data.dict(), HTTPStatus.OK)


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
    # print("REQ : ", diary_create_req)
    user_input = diary_create_req.content
    # print("USER_INPUT: ", user_input)
    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6",
        api_key_primary_val="K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q",
        request_id="b109906c-e945-4c19-9d30-8bd62bd8f0a7",
    )

    try:
        response_data = completion_executor.execute(user_input)
        # print("response data: ", response_data)
        if response_data is None:
            raise ValueError("Response data is None")

        emotions = response_data.get("emotions")
        percentage = response_data.get("percentage")
        if (emotions is None) or (percentage is None):
            raise ValueError("Emotions is None or Percentage is None")
        new_diary = DiaryCreate(user_id=current_user.id, content=user_input)
        # print("new_diary: ", new_diary)

        created_diary = await diaries_cruds.create_diary(
            session=session, diary_create=new_diary
        )

        # print("created_diary: ", created_diary)

        for emotion_enum in EmotionEnum:
            if emotion_enum.name in emotions and emotion_enum.name in percentage:

                new_emotion_react = EmotionReactCreate(
                    diary_id=created_diary.id,
                    emotion_id=emotion_enum.value,
                    content=emotions[emotion_enum.name],
                    percent=percentage[emotion_enum.name],
                )

                await emotions_reacts_cruds.create_emotion_react(
                    session=session, emotion_react_create=new_emotion_react
                )

        return create_response(True, "", response_data, HTTPStatus.CREATED)
    except (ValueError, KeyError) as e:
        return create_response(False, "Error", e, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return create_response(False, "Error", e, HTTPStatus.INTERNAL_SERVER_ERROR)


@router.get("/{diary_id}", status_code=status.HTTP_200_OK, response_model=DiaryPublic)
async def get_diary(session: SessionDep, current_user: CurrentUser, diary_id: int):
    """
    다이어리 상세 조회
    """

    diary = await diaries_cruds.get_diary_by_id(session=session, diary_id=diary_id)

    if diary is None:
        return create_response(False, "Error", None, HTTPStatus.NOT_FOUND)

    return create_response(
        True,
        "",
        DiaryPublic(
            id=diary.id,
            content=diary.content,
            chosen_emotion_id=diary.chosen_emotion_id,
            emotion_reacts=[
                EmotionReactPublic(**react.dict()) for react in diary.emotion_reacts
            ],
        ).model_dump(),
        HTTPStatus.OK,
    )


@router.patch("/{diary_id}", status_code=status.HTTP_200_OK, response_model=DiaryPublic)
async def update_diary(
    session: SessionDep,
    current_user: CurrentUser,
    diary_id: int = Path(),
    diary_update: DiaryUpdate = Body(...),
):
    """
    오늘의 메인 감정 선택
    1. id 값으로 다이어리 조히
    2. Diary의 choosen값을 고른 값으로 설정
    """
    diary = await diaries_cruds.get_diary_by_id(session=session, diary_id=diary_id)

    available_reactions = [emotion_react.id for emotion_react in diary.emotion_reacts]

    if diary_update.main_emotion_id not in available_reactions:
        return create_response(False, "Invalid emotion", None, HTTPStatus.BAD_REQUEST)

    if not diary:
        return create_response(False, "Diary not found", None, HTTPStatus.NOT_FOUND)

    update_diary = await diaries_cruds.update_main_emotion(
        session=session, diary=diary, emotion_id=diary_update.main_emotion_id
    )

    return create_response(True, "", update_diary.dict(), HTTPStatus.OK)
