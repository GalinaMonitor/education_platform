from datetime import time
from typing import List

from pydantic import parse_obj_as
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from backend.db.models import Chat as ChatDB
from backend.db.models import Course as CourseDB
from backend.db.models import CourseChapter as CourseChapterDB
from backend.db.services.base import BaseService
from backend.models import Course, CourseChapterThemes, CourseCourseChapters, CourseRead


class CourseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = CourseDB
        self.pydantic_model = Course

    async def list(self, user_id: int) -> List[CourseRead]:
        time_subquery = (
            select(CourseDB.id, func.max(ChatDB.receive_time).label("receive_time"))
            .join(CourseChapterDB, CourseChapterDB.course_id == CourseDB.id)
            .join(ChatDB, CourseChapterDB.id == ChatDB.coursechapter_id)
            .where(ChatDB.user_id == user_id)
            .group_by(CourseDB.id)
            .subquery()
        )
        statement = (
            select(CourseDB, time_subquery.c.receive_time)
            .outerjoin(time_subquery, CourseDB.id == time_subquery.c.id)
            .options(selectinload(self.model.coursechapters))
        )

        results = await self.session.execute(statement)
        results = results.all()
        parsed_results = []
        for result in results:
            parsed_result = CourseRead(**(CourseCourseChapters.from_orm(result[0]).dict()), receive_time=result[1])
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
