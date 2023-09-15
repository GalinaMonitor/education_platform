from datetime import time
from typing import List

from pydantic.tools import parse_obj_as

from src.repositories.course import CourseRepository
from src.schemas import Course, CourseChapterThemes, CourseRead
from src.services.base import BaseService


class CourseService(BaseService):
    model = Course

    def __init__(self):
        super().__init__()
        self.repo = CourseRepository()

    async def list(self, user_id: int) -> List[CourseRead]:
        return [parse_obj_as(CourseRead, course) for course in await self.repo.list(user_id)]

    async def course_chapters(self, id: int) -> List[CourseChapterThemes]:
        return [
            parse_obj_as(CourseChapterThemes, coursechapter) for coursechapter in await self.repo.course_chapters(id)
        ]

    async def change_receive_time(self, id: int, user_id, receive_time: time) -> None:
        await self.repo.change_receive_time(id, user_id, receive_time)
