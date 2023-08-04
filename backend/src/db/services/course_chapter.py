from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

import src.models as pyd_models
from src.db import models as db_models
from src.db.services.base import BaseService
from src.exceptions import NotFoundException


class CourseChapterService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = db_models.CourseChapter
        self.pydantic_model = pyd_models.CourseChapter

    async def retrieve_from_user_and_id(self, id: int, user_id: int) -> pyd_models.CourseChapterRead:
        messages_amount_subquery = (
            select(self.model.id, func.count(db_models.Message.id).label("messages_amount"))
            .join(db_models.Chat, self.model.id == db_models.Chat.coursechapter_id)
            .join(db_models.Message, db_models.Message.chat_id == db_models.Chat.id)
            .where(db_models.Chat.user_id == user_id)
            .where(self.model.id == id)
            .where(db_models.Message.is_read == False)
            .group_by(self.model.id)
            .subquery()
        )
        statement = (
            select(self.model, messages_amount_subquery.c.messages_amount)
            .outerjoin(messages_amount_subquery, self.model.id == messages_amount_subquery.c.id)
            .options(selectinload(self.model.mentor))
            .join(db_models.Chat, self.model.id == db_models.Chat.coursechapter_id)
            .where(db_models.Chat.user_id == user_id)
            .where(self.model.id == id)
        )
        results = await self.session.execute(statement)
        result = results.all()
        if not result:
            raise NotFoundException()
        result = pyd_models.CourseChapterRead(
            **(self.pydantic_model.from_orm(result[0][0]).dict()),
            messages_amount=result[0][1],
        )
        return result

    async def themes(self, id: int, user_id: int) -> List[pyd_models.ThemeRead]:
        video_amount_subquery = (
            select(
                db_models.Theme.id,
                func.count(db_models.Video.id).label("video_amount"),
                func.max(db_models.Chat.last_video).label("viewed_video_amount"),
            )
            .join(self.model, self.model.id == db_models.Theme.coursechapter_id)
            .join(db_models.Chat, self.model.id == db_models.Chat.coursechapter_id)
            .join(db_models.Video, self.model.id == db_models.Video.coursechapter_id)
            .where(db_models.Chat.user_id == user_id)
            .group_by(db_models.Theme.id)
            .subquery()
        )

        statement = (
            select(
                db_models.Theme,
                video_amount_subquery.c.video_amount,
                video_amount_subquery.c.viewed_video_amount,
            )
            .outerjoin(video_amount_subquery, db_models.Theme.id == video_amount_subquery.c.id)
            .where(db_models.Theme.coursechapter_id == id)
        )
        results = await self.session.execute(statement)
        results = results.all()
        parsed_results = []
        for result in results:
            parsed_result = pyd_models.ThemeRead(
                **(pyd_models.Theme.from_orm(result[0]).dict()),
                video_amount=result[1],
                viewed_video_amount=result[2],
            )
            parsed_results.append(parsed_result)
        return parsed_results
