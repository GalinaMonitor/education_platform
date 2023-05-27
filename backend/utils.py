import asyncio
from datetime import datetime
from time import perf_counter

from db.config import async_session
from db.services.chat import ChatService
from db.services.course import CourseService
from db.services.course_chapter import CourseChapterService
from db.services.message import MessageService
from db.services.theme import ThemeService
from db.services.user import UserService
from models import (
    AuthUser,
    ChatMessages,
    CourseChapterThemes,
    CourseCourseChapters,
    Message,
    ThemeVideos,
    UpdateUser,
    User,
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
                name=f"Test Theme {theme_id}",
                coursechapter_id=coursechapter_id,
            )
        )
        for i in range(10):
            await create_message(course_id, coursechapter_id, i, chat_id, theme.id)


async def create_course_chapter(course_id, coursechapter_id, user_id):
    async with async_session() as session:
        course_chapter = await CourseChapterService(session).create(
            CourseChapterThemes(
                name=f"Test Course {course_id} Chapter {coursechapter_id}",
                course_id=course_id,
                kinescope_project_id="b0cc85b3-63b1-4a9d-abfc-5c1e02a70daf",
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
    colors = ["#FF4343", "#10B10D", "#50D9FF"]
    async with async_session() as session:
        course = await CourseService(session).create(
            CourseCourseChapters(
                id=course_id,
                name=f"Test Course {course_id}",
                color=colors[course_id],
            )
        )
        async with asyncio.TaskGroup() as tg:
            tg.create_task(create_course_chapter(course.id, 0, user_id))
            tg.create_task(create_course_chapter(course.id, 1, user_id))
            tg.create_task(create_course_chapter(course.id, 2, user_id))


async def init_user(user: User):
    async with async_session() as session:
        chat = await ChatService(session).create(
            ChatMessages(
                user_id=user.id,
            )
        )
        await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content=f"{user.fullname if user.fullname else 'Здравствуйте'}, мне очень приятно познакомиться с вами! ",
                content_type=0,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        await MessageService(session).create(
            Message(
                datetime=datetime.now(),
                content="Позвольте мне рассказать вам дальнейшие действия. Посмотрите на левую часть экрана, именно там расположены программы, которые вы можете изучить. Просто кликните на нужный вам инструмент и выберете уровень сложности! Удачи, надеюсь вам у нас понравиться!",
                content_type=0,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        course_chapters = await CourseChapterService(session).list()
        for course_chapter in course_chapters:
            await ChatService(session).create(ChatMessages(user_id=user.id, coursechapter_id=course_chapter.id))


async def init_data():
    t0 = perf_counter()
    async with async_session() as session:
        user = await UserService(session).create(AuthUser(email="test@test.com", password="secret"))
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
