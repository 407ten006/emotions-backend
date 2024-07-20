import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    # loop.close()  # pytest_sessionfinish 함수에서 닫아준다


def pytest_sessionfinish():
    """
    https://stackoverflow.com/a/67307042
    """
    asyncio.get_event_loop().close()


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac
