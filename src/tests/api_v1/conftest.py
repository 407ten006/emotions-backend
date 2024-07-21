import asyncio
from collections.abc import Generator
from datetime import timedelta
from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlmodel import Session, SQLModel

from core import security
from core.config import settings
from core.db import engine, init_db
from core.enums import SocialProviderEnum
from main import app
from models import User
from models.auth import AuthToken
from models.users import UserCreate


@pytest.fixture()
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


def pytest_sessionfinish():
    asyncio.get_event_loop().close()


@pytest.fixture()
async def async_client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as ac:
            yield ac


@pytest.fixture()
def db_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        init_db(session, engine)
        yield session
        session.rollback()
        session.close()

    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
async def sample_user(db_session: Session):
    user_create = UserCreate(
        email="test@test.com",
        phone_number="01000000000",
        social_provider=SocialProviderEnum.naver,
    )

    user = User(**user_create.dict())

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture()
async def login_sample_user(sample_user: User):
    jwt_token = security.create_access_token(
        subject=sample_user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return AuthToken(
        access_token=jwt_token,
        token_type="bearer",
    )
