from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.settings import settings

engine = create_async_engine(settings.db_url, poolclass=NullPool)
async_session = async_sessionmaker(engine, autocommit=False, expire_on_commit=False)


@asynccontextmanager
async def get_session_context() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.commit()
            await session.close()


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.commit()
            await session.close()
