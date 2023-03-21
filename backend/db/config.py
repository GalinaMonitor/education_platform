from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from settings import settings

engine = create_async_engine(settings.db_url, echo=True)


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
