from typing import List

from pydantic.tools import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService


class ChatService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.Chat
        self.pydantic_model = pyd_models.Chat

    async def get_or_create_from_user_and_chapter(self, user_id: int, coursechapter_id: int) -> pyd_models.ChatMessages:
        statement = select(self.model).where(
            self.model.user_id == user_id,
            self.model.coursechapter_id == coursechapter_id,
        )
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            result = await ChatService(self.session).create(
                pyd_models.ChatMessages(user_id=user_id, coursechapter_id=coursechapter_id)
            )
        return result

    async def get_from_user_and_course(self, user_id: int, course_id: int) -> List[pyd_models.Chat]:
        statement = (
            select(self.model)
            .join(db_models.CourseChapter, self.model.coursechapter_id == db_models.CourseChapter.id)
            .where(db_models.CourseChapter.course_id == course_id)
            .where(
                self.model.user_id == user_id,
            )
        )

        results = await self.session.execute(statement)
        results = results.scalars().all()
        return [parse_obj_as(pyd_models.Chat, chat) for chat in results]

    async def messages(self, id: int, **kwargs) -> List[pyd_models.Message]:
        statement = select(db_models.Message).where(db_models.Message.chat_id == id)
        for key, value in kwargs.items():
            if key == "before" and value is not None:
                statement = statement.where(db_models.Message.id < value)
            elif key == "after" and value is not None:
                statement = statement.where(db_models.Message.id > value)
            elif key == "limit" and value is not None:
                statement = statement.limit(value)
            elif key == "theme" and value is not None:
                statement = statement.where(db_models.Message.theme_id == value)
        statement = statement.order_by(db_models.Message.datetime.desc())
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return [parse_obj_as(pyd_models.Message, message) for message in results]

    async def activate(self, id: int):
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        result.is_active = True
        self.session.add(result)
        await self.session.commit()

    async def deactivate(self, id: int):
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        result.is_active = False
        self.session.add(result)
        await self.session.commit()
