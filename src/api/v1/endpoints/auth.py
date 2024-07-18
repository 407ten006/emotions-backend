from fastapi import APIRouter, Depends

from src.api.v1.deps import get_oauth_client
from src.core.oauth_client import OAuthClient

router = APIRouter()


@router.get("/auth/naver-callback")
async def test_naver(code: str, state: str | None = None,
                     oauth_client: OAuthClient = Depends(get_oauth_client)) -> dict:
    token_response = await oauth_client.get_tokens(code, state)

    return {"response": token_response}
