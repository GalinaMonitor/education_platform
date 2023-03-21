from typing import List

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models.all_models import Course, CourseChapter, CourseRead
from db.services.base import BaseService


class CourseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Course

    async def list(self) -> List[CourseRead]:
        statement = select(self.model).options(selectinload(self.model.coursechapters))
        results = await self.session.exec(statement)
        result = results.all()
        return result

    async def course_chapters(self, id: int) -> List[CourseChapter]:
        statement = select(CourseChapter).where(CourseChapter.course_id == id)
        results = await self.session.exec(statement)
        result = results.all()
        return result
