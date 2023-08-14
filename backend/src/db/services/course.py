from datetime import time
from typing import List

from pydantic.tools import parse_obj_as
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService


class CourseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.Course
        self.pydantic_model = pyd_models.Course

    async def list(self, user_id: int) -> List[pyd_models.CourseRead]:
        chat_subquery = (
            select(
                self.model.id,
                func.max(db_models.CourseChapter.id).label("course_chapter_id"),
                func.max(db_models.Chat.receive_time).label("receive_time"),
                func.bool_or(db_models.Chat.is_active).label("is_active"),
            )
            .join(db_models.CourseChapter, db_models.CourseChapter.course_id == self.model.id)
            .join(db_models.Chat, db_models.CourseChapter.id == db_models.Chat.coursechapter_id)
            .where(db_models.Chat.user_id == user_id)
            .where(db_models.Chat.is_active == True)
            .group_by(self.model.id)
            .subquery()
        )
        statement = (
            select(
                self.model,
                chat_subquery.c.course_chapter_id,
                chat_subquery.c.receive_time,
                chat_subquery.c.is_active,
            )
            .outerjoin(chat_subquery, self.model.id == chat_subquery.c.id)
            .options(selectinload(self.model.coursechapters))
        )

        results = await self.session.execute(statement)
        results = results.all()
        parsed_results = []
        for result in results:
            parsed_result = pyd_models.CourseRead(
                **(pyd_models.CourseCourseChapters.model_validate(result[0]).model_dump()),
                course_chapter_id=result[1],
                receive_time=result[2],
                is_active=result[3],
            )
            parsed_results.append(parsed_result)
        return parsed_results

    async def course_chapters(self, id: int) -> List[pyd_models.CourseChapterThemes]:
        statement = select(db_models.CourseChapter).where(db_models.CourseChapter.course_id == id)
        results = await self.session.execute(statement)
        result = results.all()
        return [parse_obj_as(pyd_models.CourseChapterThemes, coursechapter) for coursechapter in result]

    async def change_receive_time(self, id: int, user_id, receive_time: time):
        statement = (
            select(db_models.Chat)
            .join(db_models.CourseChapter, db_models.Chat.coursechapter_id == db_models.CourseChapter.id)
            .where(db_models.Chat.user_id == user_id)
            .where(db_models.CourseChapter.course_id == id)
        )
        results = await self.session.execute(statement)
        results = results.scalars().all()
        for chat in results:
            chat.receive_time = receive_time
            self.session.add(chat)
        await self.session.commit()
