from api.v1.endpoints import auth, diaries, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(diaries.router, prefix="/diaries", tags=["diaries"])
