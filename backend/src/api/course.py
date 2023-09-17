from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.auth import get_current_active_user
from src.schemas import Course, CourseChapterThemes, CourseRead, Time, User
from src.services.course import CourseService
from src.services.user import UserService

router = APIRouter()


@router.get("")
async def get_courses(
    current_user: Annotated[User, Depends(get_current_active_user)],
    course_service: CourseService = Depends(CourseService),
) -> List[CourseRead]:
    return await course_service.list(user_id=current_user.id)


@router.get("/{id}")
async def get_course(id: int, course_service: CourseService = Depends(CourseService)) -> Course:
    return await course_service.retrieve(id=id)


@router.get("/{id}/course_chapters")
async def get_course_chapters(
    id: int,
    course_service: CourseService = Depends(CourseService),
) -> List[CourseChapterThemes]:
    return await course_service.course_chapters(id)


@router.post("/{id}/change_receive_time")
async def change_receive_time(
    time: Time,
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    course_service: CourseService = Depends(CourseService),
    user_service: UserService = Depends(UserService),
) -> None:
    await user_service.check_subscription(current_user)
    await course_service.change_receive_time(
        id=id,
        user_id=current_user.id,
        receive_time=datetime.strptime(time.time, "%H:%M").time(),
    )
