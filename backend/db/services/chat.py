from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models import Chat as ChatDB
from db.models import Message as MessageDB
from db.services.base import BaseService
from models import Chat, ChatMessages, Message


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = ChatDB
        self.pydantic_model = Chat

    async def get_from_user_and_chapter(self, user_id: int, coursechapter_id: int) -> ChatMessages:
        statement = select(self.model).where(
            self.model.user_id == user_id,
            self.model.coursechapter_id == coursechapter_id,
        )
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return result

    async def messages(self, id: int, **kwargs) -> List[Message]:
        statement = select(MessageDB).where(MessageDB.chat_id == id)
        for key, value in kwargs.items():
            if key == "before" and value is not None:
                statement = statement.where(MessageDB.id < value)
            elif key == "after" and value is not None:
                statement = statement.where(MessageDB.id > value)
            elif key == "limit" and value is not None:
                statement = statement.limit(value)
            elif key == "theme" and value is not None:
                statement = statement.where(MessageDB.theme_id == value)
        statement = statement.order_by(MessageDB.datetime.desc())
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return [parse_obj_as(Message, message) for message in results]
