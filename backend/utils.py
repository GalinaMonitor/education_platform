import asyncio
from datetime import datetime
from time import perf_counter

from backend.db.config import async_session
from backend.db.services.chat import ChatService
from backend.db.services.course import CourseService
from backend.db.services.course_chapter import CourseChapterService
from backend.db.services.message import MessageService
from backend.db.services.theme import ThemeService
from backend.db.services.user import UserService
from backend.models import (
    ChatMessages,
    CourseChapterThemes,
    CourseCourseChapters,
    CreateUser,
    Message,
    ThemeVideos,
    UpdateUser,
)


async def create_message(course_id, coursechapter_id, message_id, chat_id, theme_id):
    async with async_session() as session:
        await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content=f"Course {course_id} Theme {theme_id} ID {message_id}",
                content_type=0,
                chat_id=chat_id,
                theme_id=theme_id,
            )
        )


async def create_theme(theme_id, course_id, coursechapter_id, chat_id):
    async with async_session() as session:
        theme = await ThemeService(session).create(
            ThemeVideos(
                id=f"Test Theme {theme_id} Course {course_id} Course Chapter {coursechapter_id}",
                name=f"Test Theme {theme_id} Course {course_id} Course Chapter {coursechapter_id}",
                coursechapter_id=coursechapter_id,
            )
        )
        for i in range(10):
            await create_message(course_id, coursechapter_id, i, chat_id, theme.id)


async def create_course_chapter(course_id, coursechapter_id, user_id):
    colors = ["#FF4343", "#10B10D", "#50D9FF"]
    async with async_session() as session:
        course_chapter = await CourseChapterService(session).create(
            CourseChapterThemes(
                name=f"Test Course {course_id} Chapter {coursechapter_id}",
                course_id=course_id,
                kinescope_project_id="b0cc85b3-63b1-4a9d-abfc-5c1e02a70daf",
                color=colors[course_id],
            )
        )
        chat = await ChatService(session).create(ChatMessages(user_id=user_id, coursechapter_id=course_chapter.id))
        await create_theme(0, course_id, course_chapter.id, chat.id)
        await create_theme(1, course_id, course_chapter.id, chat.id)
        await create_theme(2, course_id, course_chapter.id, chat.id)
        message = await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content="https://kinescope.io/202555445",
                content_type=1,
                chat_id=chat.id,
            )
        )


async def create_course(course_id, user_id):
    async with async_session() as session:
        course = await CourseService(session).create(
            CourseCourseChapters(id=course_id, name=f"Test Course {course_id}")
        )
        async with asyncio.TaskGroup() as tg:
            tg.create_task(create_course_chapter(course.id, 0, user_id))
            tg.create_task(create_course_chapter(course.id, 1, user_id))
            tg.create_task(create_course_chapter(course.id, 2, user_id))


async def init_data():
    t0 = perf_counter()
    async with async_session() as session:
        user = await UserService(session).create(CreateUser(email="test@test.com", password="secret"))
        user = await UserService(session).update(
            id=user.id,
            data=UpdateUser(
                fullname="Test test",
                has_subscription=True,
                end_of_subscription=datetime.now().date(),
            ),
        )
        chat = await ChatService(session).create(
            ChatMessages(
                user_id=user.id,
            )
        )
        message = await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content="Test base text content",
                content_type=0,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        async with asyncio.TaskGroup() as tg:
            tg.create_task(create_course(0, user.id))
            tg.create_task(create_course(1, user.id))
            tg.create_task(create_course(2, user.id))
    print(f"Time {perf_counter() - t0}")
