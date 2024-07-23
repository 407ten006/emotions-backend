from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from starlette import status

from api.v1.deps import CurrentUser, SessionDep
from api.v1.global_response import create_response
from cruds import users as users_crud
from models.users import UserPublic, UserUpdateMe, CheckNicknamePublic

router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user_me(current_user: CurrentUser):
    """
    내 정보 조회
    """
    return create_response(True,"",jsonable_encoder(current_user))


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user_me(
    session: SessionDep,
    current_user: CurrentUser,
    user_update: UserUpdateMe = Body(...),
):
    """
    내 정보 업데이트
    """
    await users_crud.update_user(
        session=session, user=current_user, user_update=user_update
    )

    return create_response(True,"",jsonable_encoder(current_user))



@router.post(
    "/check-nickname",
    status_code=status.HTTP_200_OK,
    response_model=CheckNicknamePublic,
)
async def check_nickname(session: SessionDep, nickname: str):
    """
    유효한 닉네임 확인
    """
    # TODO: 비속어 필터 적용
    return CheckNicknamePublic(is_valid=True)
