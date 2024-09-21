import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import get_session_context
from src.repositories.chat import ChatRepository
from src.repositories.course import CourseRepository
from src.repositories.course_chapter import CourseChapterRepository
from src.repositories.message import MessageRepository
from src.repositories.theme import ThemeRepository
from src.repositories.user import UserRepository
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


async def create_message(
    course_id: int, message_id: int, chat_id: int, theme_id: str, session: AsyncSession
) -> None:
    await MessageService(MessageRepository(session=session)).create(
        Message(
            datetime=datetime.now(),
            content=f"Курс {course_id} Тема {theme_id} ID {message_id}",
            content_type=DataType.TEXT,
            chat_id=chat_id,
            theme_id=theme_id,
        )
    )


async def create_theme(
    theme_id: str,
    course_id: int,
    coursechapter_id: int,
    chat_id: int,
    session: AsyncSession,
) -> None:
    theme = await ThemeService(ThemeRepository(session=session)).create(
        ThemeVideos(
            id=f"Тема {theme_id} Курс {course_id} Уровень {coursechapter_id}",
            name=f"Тема {theme_id}",
            coursechapter_id=coursechapter_id,
        )
    )
    for i in range(10):
        await create_message(course_id, i, chat_id, theme.id, session)


async def create_course_chapter(
    course_id: int, coursechapter_id: int, user_id: int, session: AsyncSession
) -> None:
    course_chapter = await CourseChapterService(
        CourseChapterRepository(session=session)
    ).create(
        CourseChapterThemes(
            name=f"Курс {course_id} Уровень {coursechapter_id}",
            course_id=course_id,
            kinescope_project_id="b0cc85b3-63b1-4a9d-abfc-5c1e02a70daf",
        )
    )
    chat = await ChatService(ChatRepository(session=session)).create(
        ChatMessages(user_id=user_id, coursechapter_id=course_chapter.id)
    )
    await create_theme("0", course_id, course_chapter.id, chat.id, session)
    await create_theme("1", course_id, course_chapter.id, chat.id, session)
    await create_theme("2", course_id, course_chapter.id, chat.id, session)


async def create_course(course_id: int, user_id: int, session: AsyncSession) -> None:
    colors = ["#FF4343", "#10B10D", "#50D9FF"]
    course = await CourseService(CourseRepository(session=session)).create(
        Course(
            id=course_id,
            name=f"Курс {course_id}",
            color=colors[course_id],
        )
    )
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_course_chapter(course.id, 0, user_id, session))
        tg.create_task(create_course_chapter(course.id, 1, user_id, session))
        tg.create_task(create_course_chapter(course.id, 2, user_id, session))


async def init_data() -> None:
    async with get_session_context() as session:
        user_service = UserService(UserRepository(session=session))
        user = await user_service.create(
            AuthUser(email="test@test.com", password="secret")
        )
        user = await user_service.update(
            id=user.id,
            data=UpdateUser(
                fullname="Test test",
            ),
        )
        chat = await ChatService(ChatRepository(session=session)).create(
            ChatMessages(
                user_id=user.id,
            )
        )
        await MessageService(MessageRepository(session=session)).create(
            Message(
                datetime=datetime.now(),
                content="Test base text content",
                content_type=DataType.TEXT,
                chat_id=chat.id,
                theme_id=None,
            )
        )
        async with asyncio.TaskGroup() as tg:
            tg.create_task(create_course(0, user.id, session))
            tg.create_task(create_course(1, user.id, session))
            tg.create_task(create_course(2, user.id, session))
