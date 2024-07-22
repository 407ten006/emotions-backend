import json

from fastapi import APIRouter, Request, HTTPException, Body
from starlette import status

from api.v1.deps import SessionDep
from core.clova_model_api import CompletionExecutor
from cruds import emotions as emotions_cruds
from models.emotions import EmotionsPublic, EmotionPublic, EmotionCreate, EmotionUpdate

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=EmotionsPublic)
async def get_emotions(session: SessionDep):
    """
    감정 리스트 조회
    """

    emotions = await emotions_cruds.get_emotions(session=session)

    return {
        "data": emotions,
        "count": len(emotions),
    }


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmotionPublic)
async def create_emotion(
    session: SessionDep, emotion_create: EmotionCreate = Body(...)
):
    """
    감정 생성
    # TODO: 어드민 유저만 생성 가능하도록
    """

    emotion = await emotions_cruds.create_emotion(
        session=session, emotion_create=emotion_create
    )

    return emotion


@router.patch(
    "/{emotion_id}", status_code=status.HTTP_200_OK, response_model=EmotionPublic
)
async def update_emotion(
    session: SessionDep, emotion_id: int, emotion_update: EmotionUpdate = Body(...)
):
    """
    감정 수정
    """

    emotion = await emotions_cruds.get_emotion_by_id(
        session=session, emotion_id=emotion_id
    )
    if emotion is None:
        raise HTTPException(status_code=404, detail="Not Found")

    emotion = await emotions_cruds.update_emotion(
        session=session, emotion=emotion, emotion_update=emotion_update
    )

    return emotion

