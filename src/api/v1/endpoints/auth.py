from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.deps import SessionDep, get_oauth_client
from src.core import security
from src.core.config import settings
from src.core.exceptions import InvalidAuthorizationCode, InvalidToken
from src.core.oauth_client import OAuthClient
from src.cruds import users as users_crud
from src.models.auth import AuthToken, NaverLoginData
from src.models.users import SocialProvider, UserCreate

router = APIRouter()


@router.post("/naver-login")
async def naver_login(login_data: NaverLoginData, session: SessionDep,
                      oauth_client: OAuthClient = Depends(get_oauth_client)):
    try:
        token_data = await oauth_client.get_tokens(login_data.code, login_data.state)
    except InvalidAuthorizationCode:
        raise HTTPException(status_code=400, detail="Invalid authorization code")

    try:
        oauth_result = await oauth_client.get_user_info(token_data["access_token"])
        user_info = oauth_result["response"]
        user_data = {
            "email": user_info["email"],
            "id": user_info["id"],
            "mobile": user_info["mobile"],
            "name": user_info["name"],
            "profile_image": user_info["profile_image"],
            "age": user_info["age"],
            "birthday": user_info["birthday"],
            "gender": user_info["gender"]
        }

    except InvalidToken:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = users_crud.get_user_by_email(session=session, email=user_data["email"])

    if not user:
        user = users_crud.create_user(session=session, user_create=UserCreate(
            email=user_data["email"],
            phone_number=user_data["mobile"],
            social_provider=SocialProvider.naver,
        ))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_token = security.create_access_token(user.email, expires_delta=access_token_expires)

    return AuthToken(
        access_token=jwt_token,
        token_type="bearer",
    )
