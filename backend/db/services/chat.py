from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.exceptions import NotFoundException
from db.models.all_models import Message, Chat
from db.services.base import BaseService


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Chat

    async def get_from_user_and_chapter(self, user_id: int, course_chapter_id: int):
        statement = select(self.model).where(self.model.user_id == user_id,
                                             self.model.coursechapter_id == course_chapter_id)
        results = await self.session.exec(statement)
        result = results.first()
        if not result:
            raise NotFoundException()
        return result

    async def messages(self, id: int) -> List[Message]:
        statement = select(Message).where(Message.chat_id == id).order_by(Message.datetime.desc())
        results = await self.session.exec(statement)
        result = results.all()
        return result
