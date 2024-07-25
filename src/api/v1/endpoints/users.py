from api.v1.deps import CurrentUser, SessionDep
from api.v1.global_response import create_response
from core.bad_word_model_api import BadExecutor
from cruds import users as users_crud
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models.users import CheckNicknamePublic, UserPublic, UserUpdateMe
from starlette import status

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user_me(current_user: CurrentUser):
    """
    내 정보 조회
    """
    return create_response(True, "", jsonable_encoder(current_user))


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user_me(
    session: SessionDep,
    current_user: CurrentUser,
    user_update: UserUpdateMe = Body(...),
):
    """
    내 정보 업데이트
    """
    updated_user = await users_crud.update_user(
        session=session, user=current_user, user_update=user_update
    )

    return create_response(True, "", jsonable_encoder(updated_user))


@router.post(
    "/check-nickname",
    status_code=status.HTTP_200_OK,
    response_model=CheckNicknamePublic,
)
async def check_nickname(nickname: str = Body(..., embed=True)):
    """
    유효한 닉네임 확인
    """
    completion_executor = BadExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="NTA0MjU2MWZlZTcxNDJiY21itK49zPMot4GU4kpHHJ7YoRLzH63vIBpYq11WnRK6",
        api_key_primary_val="K6lejdNbv4l8otvjbazmKQHVRCfoNUKlPCwz1r2q",
        request_id="ffdfa5f8-aa09-47f5-a782-65d49637a81a",
    )

    if is_valid := completion_executor.execute(nickname):
        return create_response(
            True,
            "사용 가능한 닉네임이에요.",
            CheckNicknamePublic(is_valid=is_valid).dict(),
        )

    return create_response(
        False,
        "사용이 불가능한 닉네임이에요.",
        CheckNicknamePublic(is_valid=False).dict(),
    )
