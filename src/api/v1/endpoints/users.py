from typing import Any

from fastapi import APIRouter

from src.api.v1.deps import CurrentUser, SessionDep
from src.cruds import users as users_crud
from src.models.users import UserPublic, UserUpdateMe

router = APIRouter()


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    session: SessionDep, current_user: CurrentUser, user_update: UserUpdateMe
) -> Any:
    """
    Update current user.
    """
    users_crud.update_user(session=session, user=current_user, user_update=user_update)

    return current_user


@router.post("/check-nickname")
def check_nickname(session: SessionDep, nickname: str) -> Any:
    """
    Check nickname is already exist.
    """
    # TODO: 비속어 필터 적용
    return {
        "is_exist": users_crud.is_already_exist_nickname(
            session=session, nickname=nickname
        )
    }
