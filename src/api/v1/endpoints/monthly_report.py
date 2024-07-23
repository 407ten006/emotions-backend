from http import HTTPStatus
from typing import Any

from api.v1.deps import CurrentUser, SessionDep
from api.v1.global_response import create_response
from core.clova_model_api import CompletionExecutor
from core.report_model_api import ReportExecutor
from core.enums import EmotionEnum
from core.enums import EmotionEnum
from core.enums import get_emotion_name
from cruds import monthly_report as monthly_report_crud
from cruds import emotions_reacts as emotions_reacts_cruds
from fastapi import APIRouter, Body, Path, Query
from models.diaries import (
    DiariesMonth,
    DiaryCreate,
    DiaryCreateRequest,
    DiaryMonth,
    DiaryPublic,
    TodayDiaryPublic, DiaryUpdate,
)
from models.emotion_reacts import EmotionReactCreate, EmotionReactPublic
from starlette import status

from models.monthly_report import MonthlyReportCreateRequest, MonthlyReportCreate
from utils.utils import get_kst_today_yymmdd

router = APIRouter()



@router.post("/",  status_code=status.HTTP_200_OK)
async def create_month_report(
        session: SessionDep,
        current_user: CurrentUser,
        monthly_report_create_req: MonthlyReportCreateRequest = Body(...)

):
    create_date_yymm = monthly_report_create_req.created_date_yymm
    emotion_id = await diaries_cruds.get_most_common_emotion_for_month(
        session=session,
        user_id=current_user.id,
        search_date_yymm=create_date_yymm
    )
    emotion_name = get_emotion_name(emotion_id)

    completion_executor = ReportExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6',
        api_key_primary_val='K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q',
        request_id='ffdfa5f8-aa09-47f5-a782-65d49637a81a'
    )

    result = completion_executor.execute(emotion_name)

    monthly_report = MonthlyReportCreate(user_id=current_user.id, content=result, created_date_yymm = create_date_yymm)
    return create_response(True,"",monthly_report.dict(),HTTPStatus.CREATED)

@router.post("/{created_date}",  status_code=status.HTTP_200_OK)
async def get_monthly_report(
        session: SessionDep,
        current_user: CurrentUser,
        created_date: str
):
    monthly_report = await monthly_report_crud.get_monthly_report_by_date(
        session=session,
        user_id=current_user.id,
        created_date_yymm=created_date
    )

    if monthly_report is not None:
        return create_response(True,"",monthly_report.dict(),HTTPStatus.OK)
    else:
        return create_response(False,"Error",None,HTTPStatus.NOT_FOUND)