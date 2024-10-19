from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous generator function to create an AsyncSession for database operations.

    Yields:
        AsyncSession: An asynchronous session for database operations.
    """
    async with async_session_maker() as session:
        yield session
