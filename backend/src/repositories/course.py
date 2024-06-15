from datetime import time
from typing import List

from sqlalchemy import func, select

from src.db.config import async_session
from src.db.models import Chat, Course, CourseChapter
from src.repositories.base import BaseRepository
from src.repositories.course_chapter import CourseChapterRepository


class CourseRepository(BaseRepository):
    model = Course

    async def list(self, user_id: int) -> List[dict]:
        chat_subquery = (
            select(
                self.model.id,
                func.max(CourseChapter.id).label("course_chapter_id"),
                func.max(Chat.receive_time).label("receive_time"),
                func.bool_or(Chat.is_active).label("is_active"),
            )
            .join(CourseChapter, CourseChapter.course_id == self.model.id)
            .join(Chat, CourseChapter.id == Chat.coursechapter_id)
            .where(Chat.user_id == user_id)
            .where(Chat.is_active == True)
            .group_by(self.model.id)
            .subquery()
        )
        statement = select(
            self.model.__table__.columns,
            chat_subquery.c.course_chapter_id,
            chat_subquery.c.receive_time,
            chat_subquery.c.is_active,
        ).outerjoin(chat_subquery, self.model.id == chat_subquery.c.id)
        results = await self._session.execute(statement)
        results = results.mappings().all()
        courses_with_coursechapters = []
        coursechapter_repo = CourseChapterRepository(self._session)
        for result in results:
            result = dict(result)
            result["coursechapters"] = await coursechapter_repo.list(course_id=result["id"])
            courses_with_coursechapters.append(result)
        return courses_with_coursechapters

    async def change_receive_time(self, id: int, user_id, receive_time: time) -> None:
        statement = (
            select(Chat)
            .join(CourseChapter, Chat.coursechapter_id == CourseChapter.id)
            .where(Chat.user_id == user_id)
            .where(CourseChapter.course_id == id)
        )
        results = await self._session.execute(statement)
        results = results.scalars().all()
        for chat in results:
            chat.receive_time = receive_time
            self._session.add(chat)
        await self._session.flush()
