import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from src.app import app
from src.config import DB_NAME_TEST, DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST
from src.database import Base, get_async_session

DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)
