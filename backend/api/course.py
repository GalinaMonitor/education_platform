from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db.config import get_session
from db.models.all_models import CourseChapter, Course, CourseRead
from db.services.course import CourseService

router = APIRouter()


@router.get('/')
async def get_courses(session: AsyncSession = Depends(get_session)) -> List[CourseRead]:
    return await CourseService(session).list()


@router.get('/{id}/course_chapters')
async def get_course_chapters(id: int, session: AsyncSession = Depends(get_session)) -> List[CourseChapter]:
    return await CourseService(session).course_chapters(id)
