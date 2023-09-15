from sqlalchemy import func, select

from src.db.config import async_session
from src.db.models import Chat, User
from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    async def get_by_email(self, email: str) -> dict:
        async with async_session() as session:
            statement = select(self.model).where(self.model.email == email)
            results = await session.execute(statement)
            result = results.scalar_one_or_none()
            if not result:
                raise NotFoundException()
            return result

    async def get_base_chat(self, id: int) -> dict:
        async with async_session() as session:
            statement = select(Chat).where(Chat.user_id == id, Chat.coursechapter_id == None)
            results = await session.execute(statement)
            result = results.scalar_one_or_none()
            if not result:
                raise NotFoundException()
            return result

    async def get_total_users(self) -> int:
        async with async_session() as session:
            statement = select(func.count(self.model.id))
            results = await session.execute(statement)
            result = results.scalar_one_or_none()
            return result
