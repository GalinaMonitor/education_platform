from typing import List

from sqlalchemy import select

from src.db.models import Chat, CourseChapter, Message
from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository
from src.schemas import ChatType, PaginationParams


class ChatRepository(BaseRepository):
    model = Chat

    async def get_from_user_and_chapter(
        self, user_id: int, coursechapter_id: int
    ) -> List[dict]:
        statement = select(self.model).where(
            self.model.user_id == user_id,
            self.model.coursechapter_id == coursechapter_id,
            self.model.chat_type == ChatType.COURSE,
        )
        results = await self._session.execute(statement)
        result = results.scalar_one_or_none()
        if not result:
            raise NotFoundException()
        return result

    async def get_from_user_and_course(
        self, user_id: int, course_id: int
    ) -> List[dict]:
        statement = (
            select(self.model)
            .join(CourseChapter, self.model.coursechapter_id == CourseChapter.id)
            .where(
                CourseChapter.course_id == course_id,
                self.model.user_id == user_id,
                self.model.chat_type == ChatType.COURSE,
            )
        )
        results = await self._session.execute(statement)
        results = results.scalars().all()
        return results

    async def messages(
        self,
        id: int,
        pagination_params: PaginationParams | None = None,
        theme_id: str | None = None,
    ) -> List[dict]:
        statement = select(Message).where(Message.chat_id == id)
        reverse = False
        if pagination_params:
            if pagination_params.before is not None:
                statement = statement.where(Message.id < pagination_params.before)
            if pagination_params.after is not None:
                statement = statement.where(Message.id > pagination_params.after)
            if pagination_params.limit is not None:
                statement = statement.limit(pagination_params.limit)
        if theme_id:
            statement = statement.where(Message.theme_id == theme_id)
        if (
            pagination_params
            and pagination_params.limit is not None
            and pagination_params.after is not None
        ):
            order_by = Message.datetime
            reverse = True
        else:
            order_by = Message.datetime.desc()
        statement = statement.order_by(order_by)
        results = await self._session.execute(statement)
        results = results.scalars().all()
        if reverse:
            results = reversed(results)
        return results
