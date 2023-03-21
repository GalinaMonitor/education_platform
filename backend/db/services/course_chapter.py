from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from db.models.all_models import Message, CourseChapter, Theme
from db.services.base import BaseService


class CourseChapterService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = CourseChapter

    async def themes(self, id: int) -> List[Theme]:
        statement = select(Theme).where(Theme.course_chapter_id == id)
        results = await self.session.exec(statement)
        result = results.all()
        return result
