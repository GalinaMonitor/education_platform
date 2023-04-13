from datetime import time
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models import Chat, Course, CourseChapter
from db.services.base import BaseService
from models import CourseRead


class CourseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Course

    async def list(self, user_id: int) -> List[CourseRead]:
        time_subquery = (
            select(Course.id, func.max(Chat.receive_time).label("receive_time"))
            .join(CourseChapter, CourseChapter.course_id == Course.id)
            .join(Chat, CourseChapter.id == Chat.coursechapter_id)
            .where(Chat.user_id == user_id)
            .group_by(Course.id)
            .subquery()
        )
        statement = (
            select(Course, time_subquery.c.receive_time)
            .outerjoin(time_subquery, Course.id == time_subquery.c.id)
            .options(selectinload(self.model.coursechapters))
        )

        results = await self.session.exec(statement)
        results = results.all()
        parsed_results = []
        print(results)
        for result in results:
            parsed_result = CourseRead(
                **result[0].dict(), coursechapters=result[0].coursechapters, receive_time=result[1]
            )
            parsed_results.append(parsed_result)
        print(results)
        return parsed_results

    async def course_chapters(self, id: int) -> List[CourseChapter]:
        statement = select(CourseChapter).where(CourseChapter.course_id == id)
        results = await self.session.exec(statement)
        result = results.all()
        return result

    async def change_receive_time(self, id: int, user_id, receive_time: time):
        statement = (
            select(Chat)
            .join(CourseChapter, Chat.coursechapter_id == CourseChapter.id)
            .where(Chat.user_id == user_id)
            .where(CourseChapter.course_id == id)
        )
        results = await self.session.exec(statement)
        results = results.all()
        for chat in results:
            chat.receive_time = receive_time
            self.session.add(chat)
        await self.session.commit()
