from datetime import time
from typing import List

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.db.config import async_session
from src.db.models import Chat, Course, CourseChapter
from src.repositories.base import BaseRepository


class CourseRepository(BaseRepository):
    model = Course

    async def list(self, user_id: int) -> List[dict]:
        async with async_session() as session:
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
            statement = (
                select(
                    self.model,
                    chat_subquery.c.course_chapter_id,
                    chat_subquery.c.receive_time,
                    chat_subquery.c.is_active,
                )
                .outerjoin(chat_subquery, self.model.id == chat_subquery.c.id)
                .options(selectinload(self.model.coursechapters))
            )

            results = await session.execute(statement)
            results = results.all()
            parsed_results = []
            for result in results:
                parsed_result = {
                    **result[0],
                    "course_chapter_id": result[1],
                    "receive_time": result[2],
                    "is_active": result[3],
                }
                parsed_results.append(parsed_result)
            return parsed_results

    async def course_chapters(self, id: int) -> List[dict]:
        async with async_session() as session:
            statement = select(CourseChapter).where(CourseChapter.course_id == id)
            results = await session.execute(statement)
            result = results.all()
            return result

    async def change_receive_time(self, id: int, user_id, receive_time: time) -> None:
        async with async_session() as session:
            statement = (
                select(Chat)
                .join(CourseChapter, Chat.coursechapter_id == CourseChapter.id)
                .where(Chat.user_id == user_id)
                .where(CourseChapter.course_id == id)
            )
            results = await session.execute(statement)
            results = results.scalars().all()
            for chat in results:
                chat.receive_time = receive_time
                session.add(chat)
            await session.commit()
