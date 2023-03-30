from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from auth import get_current_active_user
from db.config import get_session
from db.models import CourseChapter, User
from db.services.course import CourseService
from models import CourseRead, Time

router = APIRouter()


@router.get("")
async def get_courses(session: AsyncSession = Depends(get_session)) -> List[CourseRead]:
    return await CourseService(session).list()


@router.get("/{id}/course_chapters")
async def get_course_chapters(id: int, session: AsyncSession = Depends(get_session)) -> List[CourseChapter]:
    return await CourseService(session).course_chapters(id)


@router.post("/{id}/change_receive_time")
async def change_receive_time(
    time: Time,
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    time = datetime.strptime(time.time, "%H:%M").time()
    await CourseService(session).change_receive_time(id, user_id=current_user.id, receive_time=time)
    return "Success"
