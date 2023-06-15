from typing import List

from pydantic import parse_obj_as
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from db.exceptions import NotFoundException
from db.models import Chat as ChatDB
from db.models import CourseChapter as CourseChapterDB
from db.models import Theme as ThemeDB
from db.models import Video as VideoDB
from db.services.base import BaseService
from models import CourseChapter, CourseChapterThemes, Theme, ThemeRead


class CourseChapterService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = CourseChapterDB
        self.pydantic_model = CourseChapter

    async def retrieve_from_user_and_id(self, id: int, user_id: int) -> CourseChapter:
        statement = (
            select(
                CourseChapterDB,
            )
            .join(ChatDB, CourseChapterDB.id == ChatDB.coursechapter_id)
            .where(ChatDB.user_id == user_id)
            .where(CourseChapterDB.id == id)
        )
        results = await self.session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return self.pydantic_model.from_orm(result)

    async def themes(self, id: int, user_id: int) -> List[ThemeRead]:
        video_amount_subquery = (
            select(
                ThemeDB.id,
                func.count(VideoDB.id).label("video_amount"),
                func.max(ChatDB.last_video).label("viewed_video_amount"),
            )
            .join(CourseChapterDB, CourseChapterDB.id == ThemeDB.coursechapter_id)
            .join(ChatDB, CourseChapterDB.id == ChatDB.coursechapter_id)
            .join(VideoDB, CourseChapterDB.id == VideoDB.coursechapter_id)
            .where(ChatDB.user_id == user_id)
            .group_by(ThemeDB.id)
            .subquery()
        )

        statement = (
            select(
                ThemeDB,
                video_amount_subquery.c.video_amount,
                video_amount_subquery.c.viewed_video_amount,
            )
            .outerjoin(video_amount_subquery, ThemeDB.id == video_amount_subquery.c.id)
            .where(ThemeDB.coursechapter_id == id)
        )
        results = await self.session.execute(statement)
        results = results.all()
        parsed_results = []
        for result in results:
            parsed_result = ThemeRead(
                **(Theme.from_orm(result[0]).dict()),
                video_amount=result[1],
                viewed_video_amount=result[2],
            )
            parsed_results.append(parsed_result)
        return parsed_results
