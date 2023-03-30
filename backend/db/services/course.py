from datetime import time
from typing import List

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

    async def list(self) -> List[CourseRead]:
        statement = select(self.model).options(selectinload(self.model.coursechapters))
        results = await self.session.exec(statement)
        results = results.all()
        return results

    async def course_chapters(self, id: int) -> List[CourseChapter]:
        statement = select(CourseChapter).where(CourseChapter.course_id == id)
        results = await self.session.exec(statement)
        result = results.all()
        return result

    async def change_receive_time(self, id: int, user_id, receive_time: time):
        statement = (
            select(Chat)
            .join(CourseChapter)
            .where(
                Chat.user_id == user_id and CourseChapter.course_id == id and Chat.coursechapter_id == CourseChapter.id
            )
        )
        results = await self.session.exec(statement)
        results = results.all()
        print(results)
        for chat in results:
            chat.receive_time = receive_time
            self.session.add(chat)
        await self.session.commit()
