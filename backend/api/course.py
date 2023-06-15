from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from auth import get_current_active_user
from db.config import get_session
from db.services.course import CourseService
from exceptions import HasNoSubscriptionException
from models import Course, CourseChapterThemes, CourseRead, Time, User

router = APIRouter()


@router.get("")
async def get_courses(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
) -> List[CourseRead]:
    return await CourseService(session).list(user_id=current_user.id)


@router.get("/{id}")
async def get_course(
    id: int,
    session: AsyncSession = Depends(get_session),
) -> Course:
    return await CourseService(session).retrieve(id=id)


@router.get("/{id}/course_chapters")
async def get_course_chapters(id: int, session: AsyncSession = Depends(get_session)) -> List[CourseChapterThemes]:
    return await CourseService(session).course_chapters(id)


@router.post("/{id}/change_receive_time")
async def change_receive_time(
    time: Time,
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    if not current_user.has_subscription:
        raise HasNoSubscriptionException
    time = datetime.strptime(time.time, "%H:%M").time()
    return await CourseService(session).change_receive_time(id=id, user_id=current_user.id, receive_time=time)
