from sqlalchemy import func, select

from src.db.models import Chat, User
from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository
from src.schemas import ChatType


class UserRepository(BaseRepository):
    model = User

    async def get_by_email(self, email: str) -> dict:
        statement = select(self.model).where(self.model.email == email)
        results = await self._session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return result

    async def get_base_chat(self, id: int) -> dict:
        statement = select(Chat).where(
            Chat.user_id == id,
            Chat.coursechapter_id is None,
            Chat.chat_type == ChatType.MAIN,
        )
        results = await self._session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return result

    async def get_total_users(self) -> int:
        statement = select(func.count(self.model.id))
        results = await self._session.execute(statement)
        result = results.scalar_one_or_none()
        return result
