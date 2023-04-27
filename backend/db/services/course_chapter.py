from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from backend.db.models import CourseChapter as CourseChapterDB
from backend.db.models import Theme as ThemeDB
from backend.db.services.base import BaseService
from backend.models import CourseChapter, CourseChapterThemes, Theme


class CourseChapterService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = CourseChapterDB
        self.pydantic_model = CourseChapter

    async def themes(self, id: int) -> List[Theme]:
        statement = select(ThemeDB).where(ThemeDB.coursechapter_id == id)
        results = await self.session.execute(statement)
        results = results.scalars().all()
        return [parse_obj_as(Theme, theme) for theme in results]
