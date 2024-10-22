from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings
from src.core.db import BaseORM
from src.deps import get_db
from src.main import app
from src.users.models import User

engine_test = create_async_engine(
    settings.SQLALCHEMY_TEST_DATABASE_URI,
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(autouse=True, scope="function")
async def prepare_database() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.rollback()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/api"
    ) as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def create_list_users(async_client: AsyncClient):
    user_list_register_today = [
        User(
            username=f"user_first_group{n}",
            email=f"user_first_group{n}@example.com",
            registration=datetime.now(),
        )
        for n in range(13)
    ]

    user_list_register_three_days_ago = [
        User(
            username=f"user_second_group{n}",
            email=f"user_second_group{n}@gmail.com",
            registration=datetime.now() - timedelta(days=3),
        )
        for n in range(7)
    ]

    user_list_register_more_than_seven_days_ago = [
        User(
            username=f"user_third_group{n}",
            email=f"user_third_group{n}@yandex.ru",
            registration=datetime.now() - timedelta(days=10),
        )
        for n in range(5)
    ]

    async with async_session_maker() as session:
        session.add_all(user_list_register_today)
        session.add_all(user_list_register_three_days_ago)
        session.add_all(user_list_register_more_than_seven_days_ago)
        await session.commit()
    return (
        *user_list_register_today,
        *user_list_register_three_days_ago,
        *user_list_register_more_than_seven_days_ago,
    )
