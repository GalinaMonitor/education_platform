import asyncio
from datetime import datetime

from src.schemas import (
    AuthUser,
    ChatMessages,
    Course,
    CourseChapterThemes,
    DataType,
    Message,
    ThemeVideos,
    UpdateUser,
)
from src.services.chat import ChatService
from src.services.course import CourseService
from src.services.course_chapter import CourseChapterService
from src.services.message import MessageService
from src.services.theme import ThemeService
from src.services.user import UserService


async def create_message(course_id: int, message_id: int, chat_id: int, theme_id: str) -> None:
    await MessageService().create(
        Message(
            datetime=datetime.now(),
            content=f"Курс {course_id} Тема {theme_id} ID {message_id}",
            content_type=DataType.TEXT,
            chat_id=chat_id,
            theme_id=theme_id,
        )
    )


async def create_theme(theme_id: str, course_id: int, coursechapter_id: int, chat_id: int) -> None:
    theme = await ThemeService().create(
        ThemeVideos(
            id=f"Тема {theme_id} Курс {course_id} Уровень {coursechapter_id}",
            name=f"Тема {theme_id}",
            coursechapter_id=coursechapter_id,
        )
    )
    for i in range(10):
        await create_message(course_id, i, chat_id, theme.id)


async def create_course_chapter(course_id: int, coursechapter_id: int, user_id: int) -> None:
    course_chapter = await CourseChapterService().create(
        CourseChapterThemes(
            name=f"Курс {course_id} Уровень {coursechapter_id}",
            course_id=course_id,
            kinescope_project_id="b0cc85b3-63b1-4a9d-abfc-5c1e02a70daf",
        )
    )
    chat = await ChatService().create(ChatMessages(user_id=user_id, coursechapter_id=course_chapter.id))
    await create_theme("0", course_id, course_chapter.id, chat.id)
    await create_theme("1", course_id, course_chapter.id, chat.id)
    await create_theme("2", course_id, course_chapter.id, chat.id)


async def create_course(course_id: int, user_id: int) -> None:
    colors = ["#FF4343", "#10B10D", "#50D9FF"]
    course = await CourseService().create(
        Course(
            id=course_id,
            name=f"Курс {course_id}",
            color=colors[course_id],
        )
    )
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_course_chapter(course.id, 0, user_id))
        tg.create_task(create_course_chapter(course.id, 1, user_id))
        tg.create_task(create_course_chapter(course.id, 2, user_id))


async def init_data() -> None:
    user = await UserService().create(AuthUser(email="test@test.com", password="secret"))
    user = await UserService().update(
        id=user.id,
        data=UpdateUser(
            fullname="Test test",
        ),
    )
    chat = await ChatService().create(
        ChatMessages(
            user_id=user.id,
        )
    )
    message = await MessageService().create(
        Message(
            datetime=datetime.now(),
            content="Test base text content",
            content_type=DataType.TEXT,
            chat_id=chat.id,
            theme_id=None,
        )
    )
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_course(0, user.id))
        tg.create_task(create_course(1, user.id))
        tg.create_task(create_course(2, user.id))
