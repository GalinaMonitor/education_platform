from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic.tools import parse_obj_as

from src.exceptions import NotFoundException
from src.repositories.chat import ChatRepository
from src.repositories.message import MessageRepository
from src.schemas import (
    Chat,
    ChatMessages,
    ChatType,
    CourseChapter,
    DataType,
    Message,
    PaginationParams,
    User,
)
from src.services.base import BaseService


class ChatService(BaseService):
    model = Chat

    def __init__(self, repo: ChatRepository = Depends()):
        super().__init__()
        self.repo = repo

    async def get_or_create_from_user_and_chapter(self, user_id: int, coursechapter_id: int) -> Chat:
        try:
            result = await self.repo.get_from_user_and_chapter(user_id, coursechapter_id)
        except NotFoundException:
            result = await self.repo.create(
                ChatMessages(user_id=user_id, coursechapter_id=coursechapter_id, chat_type=ChatType.COURSE).model_dump()
            )
        return self.model.model_validate(result)

    async def get_from_user_and_course(self, user_id: int, course_id: int) -> List[Chat]:
        return [parse_obj_as(Chat, chat) for chat in await self.repo.get_from_user_and_course(user_id, course_id)]

    async def messages(
        self, id: int, pagination_params: PaginationParams | None = None, theme_id: str | None = None
    ) -> List[Message]:
        return parse_obj_as(list[Message], await self.repo.messages(id, pagination_params, theme_id))

    async def activate(self, chat: Chat, user: User, coursechapter: CourseChapter) -> None:
        from src.async_tasks.celery_config import send_video
        from src.services.message import MessageService

        if not chat.get_welcome_message:
            await MessageService(MessageRepository(self.repo._session)).create(
                Message(
                    datetime=datetime.now(),
                    content=f"Ку, {user.fullname}! " + coursechapter.welcome_message
                    if user.fullname
                    else "Ку! " + coursechapter.welcome_message,
                    content_type=DataType.TEXT,
                    chat_id=chat.id,
                    theme_id=None,
                )
            )
            await self.repo.update(chat.id, {"get_welcome_message": True})
            for _ in range(5):
                await send_video(email=user.email, coursechapter_id=coursechapter.id)
        all_chats = await self.get_from_user_and_course(user_id=user.id, course_id=coursechapter.course_id)
        await self.repo.update(chat.id, {"is_active": True})
        for deactivate_chat in all_chats:
            if deactivate_chat.id != chat.id:
                await self.repo.update(deactivate_chat.id, {"is_active": False})
