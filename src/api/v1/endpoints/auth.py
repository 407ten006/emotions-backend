from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.deps import get_oauth_client
from src.core.exceptions import InvalidAuthorizationCode, InvalidToken
from src.core.oauth_client import OAuthClient
from src.models.auth import NaverLoginData

router = APIRouter()


@router.post("/auth/naver-login")
async def naver_login(login_data: NaverLoginData, oauth_client: OAuthClient = Depends(get_oauth_client)):
    try:
        token_data = await oauth_client.get_tokens(login_data.code, login_data.state)
    except InvalidAuthorizationCode:
        raise HTTPException(status_code=400, detail="토큰 교환 실패")

    try:
        user_data = await oauth_client.get_user_info(token_data["access_token"])
    except InvalidToken:
        raise HTTPException(status_code=400, detail="사용자 정보 가져오기 실패")

    # TODO: 자동 회원 가입

    # TODO: JWT 토큰 생성
    # jwt_token = create_jwt_token(user_data)
    return {"user_data": user_data}
