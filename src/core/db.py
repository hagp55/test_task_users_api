from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class BaseORM(DeclarativeBase):
    pass
