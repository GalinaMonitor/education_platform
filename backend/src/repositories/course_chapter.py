from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.db.config import async_session
from src.db.models import Chat, CourseChapter, Message, Theme, Video
from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository


class CourseChapterRepository(BaseRepository):
    model = CourseChapter

    async def retrieve_from_user_and_id(self, id: int, user_id: int) -> dict:
        async with async_session() as session:
            messages_amount_subquery = (
                select(self.model.id, func.count(Message.id).label("messages_amount"))
                .join(Chat, self.model.id == Chat.coursechapter_id)
                .join(Message, Message.chat_id == Chat.id)
                .where(Chat.user_id == user_id)
                .where(self.model.id == id)
                .where(Message.is_read == False)
                .group_by(self.model.id)
                .subquery()
            )
            statement = (
                select(self.model, messages_amount_subquery.c.messages_amount)
                .outerjoin(messages_amount_subquery, self.model.id == messages_amount_subquery.c.id)
                .options(selectinload(self.model.mentor))
                .join(Chat, self.model.id == Chat.coursechapter_id)
                .where(Chat.user_id == user_id)
                .where(self.model.id == id)
            )
            results = await session.execute(statement)
            result = results.all()
            if not result:
                raise NotFoundException()
            result = {
                **result[0][0],
                "messages_amount": result[0][1],
            }
            return result

    async def themes(self, id: int, user_id: int) -> List[dict]:
        async with async_session() as session:
            video_amount_subquery = (
                select(
                    Theme.id,
                    func.count(Video.id).label("video_amount"),
                    func.max(Chat.last_video).label("viewed_video_amount"),
                )
                .join(self.model, self.model.id == Theme.coursechapter_id)
                .join(Chat, self.model.id == Chat.coursechapter_id)
                .join(Video, Theme.id == Video.theme_id)
                .where(Chat.user_id == user_id)
                .group_by(Theme.id)
                .subquery()
            )

            statement = (
                select(
                    Theme,
                    video_amount_subquery.c.video_amount,
                    video_amount_subquery.c.viewed_video_amount,
                )
                .outerjoin(video_amount_subquery, Theme.id == video_amount_subquery.c.id)
                .where(Theme.coursechapter_id == id)
            )
            results = await session.execute(statement)
            results = results.all()
            parsed_results = []
            for result in results:
                parsed_result = {
                    **result[0],
                    "video_amount": result[1],
                    "viewed_video_amount": result[2],
                }
                parsed_results.append(parsed_result)
            return parsed_results
