from datetime import time
from typing import List

from pydantic import parse_obj_as
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Chat as ChatDB
from db.models import Course as CourseDB
from db.models import CourseChapter as CourseChapterDB
from db.services.base import BaseService
from models import Course, CourseChapterThemes, CourseCourseChapters, CourseRead


class CourseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = CourseDB
        self.pydantic_model = Course

    async def list(self, user_id: int) -> List[CourseRead]:
        chat_subquery = (
            select(
                CourseDB.id,
                func.max(CourseChapterDB.id).label("course_chapter_id"),
                func.max(ChatDB.receive_time).label("receive_time"),
                func.bool_or(ChatDB.is_active).label("is_active"),
            )
            .join(CourseChapterDB, CourseChapterDB.course_id == CourseDB.id)
            .join(ChatDB, CourseChapterDB.id == ChatDB.coursechapter_id)
            .where(ChatDB.user_id == user_id)
            .where(ChatDB.is_active == True)
            .group_by(CourseDB.id)
            .subquery()
        )
        statement = (
            select(
                CourseDB,
                chat_subquery.c.course_chapter_id,
                chat_subquery.c.receive_time,
                chat_subquery.c.is_active,
            )
            .outerjoin(chat_subquery, CourseDB.id == chat_subquery.c.id)
            .options(selectinload(self.model.coursechapters))
        )

        results = await self.session.execute(statement)
        results = results.all()
        parsed_results = []
        for result in results:
            parsed_result = CourseRead(
                **(CourseCourseChapters.from_orm(result[0]).dict()),
                course_chapter_id=result[1],
                receive_time=result[2],
                is_active=result[3],
            )
            parsed_results.append(parsed_result)
        return parsed_results

    async def course_chapters(self, id: int) -> List[CourseChapterThemes]:
        statement = select(CourseChapterDB).where(CourseChapterDB.course_id == id)
        results = await self.session.execute(statement)
        result = results.all()
        return [parse_obj_as(CourseChapterThemes, coursechapter) for coursechapter in result]

    async def change_receive_time(self, id: int, user_id, receive_time: time):
        statement = (
            select(ChatDB)
            .join(CourseChapterDB, ChatDB.coursechapter_id == CourseChapterDB.id)
            .where(ChatDB.user_id == user_id)
            .where(CourseChapterDB.course_id == id)
        )
        results = await self.session.execute(statement)
        results = results.scalars().all()
        for chat in results:
            chat.receive_time = receive_time
            self.session.add(chat)
        await self.session.commit()
