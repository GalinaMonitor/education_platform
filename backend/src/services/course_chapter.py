from typing import List

from fastapi import Depends
from pydantic.tools import parse_obj_as

from src.repositories.course_chapter import CourseChapterRepository
from src.schemas import CourseChapter, CourseChapterRead, ThemeRead
from src.services.base import BaseService


class CourseChapterService(BaseService):
    model = CourseChapter

    def __init__(self, repo: CourseChapterRepository = Depends()):
        super().__init__()
        self.repo = repo

    async def retrieve_from_user_and_id(
        self, id: int, user_id: int
    ) -> CourseChapterRead:
        return CourseChapterRead.model_validate(
            await self.repo.retrieve_from_user_and_id(id, user_id)
        )

    async def themes(self, id: int, user_id: int) -> List[ThemeRead]:
        results = [
            parse_obj_as(ThemeRead, theme)
            for theme in await self.repo.themes(id, user_id)
        ]
        # TODO Transform into sql
        if results:
            total_viewed_video = results[0].viewed_video_amount
            for theme in results:
                if theme.viewed_video_amount:
                    theme.viewed_video_amount = (
                        theme.video_amount
                        if theme.video_amount <= total_viewed_video
                        else total_viewed_video
                    )
                else:
                    theme.viewed_video_amount = 0
                if theme.video_amount >= total_viewed_video:
                    total_viewed_video = 0
                else:
                    total_viewed_video -= theme.video_amount
        return results
