import asyncio
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import get_session_context
from src.exceptions import HasNoSubscriptionException, NotFoundException
from src.kinescope.api import KinescopeClient
from src.repositories.chat import ChatRepository
from src.repositories.course_chapter import CourseChapterRepository
from src.repositories.message import MessageRepository
from src.repositories.theme import ThemeRepository
from src.repositories.user import UserRepository
from src.repositories.video import VideoRepository
from src.schemas import (
    AuthUser,
    Chat,
    DataType,
    Message,
    SubscriptionType,
    Theme,
    UpdateUser,
    Video,
)
from src.services.mail import MailService
from src.settings import settings
from src.text_constants import SUBSCRIPTION_END_MESSAGE, SUBSCRIPTION_LAST_DAY_MESSAGE

celery_app = Celery(
    broker=settings.redis_url,
    redis_max_connections=3,
    result_persistent=True,
    enable_ut=True,
    timezone="Europe/Moscow",
    redis_socket_timeout=15,
    event_serializer="json",
    task_serializer="json",
    acks_late=True,
    prefetch_multiplier=1,
    create_missing_queues=True,
    backend=settings.redis_url,
)


async def sync_kinescope() -> None:
    from src.services.course_chapter import CourseChapterService
    from src.services.theme import ThemeService
    from src.services.video import VideoService

    async with get_session_context() as session:
        theme_service = ThemeService(ThemeRepository(session))
        coursechapter_service = CourseChapterService(CourseChapterRepository(session))
        video_service = VideoService(VideoRepository(session))

        course_chapters = await coursechapter_service.list()
        for course_chapter in course_chapters:
            if not course_chapter.kinescope_project_id:
                continue
            video_list = KinescopeClient().get_project_video_list(course_chapter.kinescope_project_id)
            for video in video_list:
                if video.folder_id:
                    try:
                        theme = await theme_service.retrieve(id=video.folder_id)
                    except NotFoundException:
                        theme = await theme_service.create(
                            data=Theme(
                                id=video.folder_id,
                                name=video.folder_name,
                                coursechapter_id=course_chapter.id,
                            )
                        )
                else:
                    theme = None
                try:
                    order = int(video.title.split(". ")[0])
                except Exception:
                    continue
                try:
                    db_video = await video_service.retrieve(id=video.id)
                    await video_service.update(
                        id=db_video.id,
                        data=Video(
                            id=db_video.id,
                            order=order,
                            description=video.description,
                            name=video.title,
                            link=video.play_link,
                            coursechapter_id=course_chapter.id,
                            theme_id=theme.id if theme else None,
                        ),
                    )
                except NotFoundException:
                    await video_service.create(
                        data=Video(
                            id=video.id,
                            order=order,
                            description=video.description,
                            name=video.title,
                            link=video.play_link,
                            coursechapter_id=course_chapter.id,
                            theme_id=theme.id if theme else None,
                        )
                    )
        session.commit()


@celery_app.task
def sync_kinescope_task() -> None:
    asyncio.run(sync_kinescope())


async def send_video(email: str, coursechapter_id: int, session: AsyncSession) -> None:
    from src.services.chat import ChatService
    from src.services.course_chapter import CourseChapterService
    from src.services.message import MessageService
    from src.services.user import UserService
    from src.services.video import VideoService

    coursechapter_service = CourseChapterService(CourseChapterRepository(session))
    video_service = VideoService(VideoRepository(session))
    chat_service = ChatService(ChatRepository(session))
    user_service = UserService(UserRepository(session))
    message_service = MessageService(MessageRepository(session))

    user = await user_service.get_by_email(email)
    chat = await chat_service.get_or_create_from_user_and_chapter(user_id=user.id, coursechapter_id=coursechapter_id)
    new_video = await video_service.list(coursechapter_id=chat.coursechapter_id, order=chat.last_video + 1)
    if new_video:
        new_video = new_video[0]
    else:
        return
    await message_service.create(
        Message(
            datetime=datetime.now(),
            content=f"{new_video.name}\n{new_video.description}",
            content_type=DataType.TEXT,
            chat_id=chat.id,
            theme_id=new_video.theme_id,
        )
    )
    await message_service.create(
        Message(
            datetime=datetime.now(),
            content=new_video.link,
            content_type=DataType.VIDEO,
            chat_id=chat.id,
            theme_id=new_video.theme_id,
        )
    )
    await chat_service.update(id=chat.id, data=Chat(last_video=chat.last_video + 1))
    coursechapter = await coursechapter_service.retrieve(id=chat.coursechapter_id)
    user = await user_service.retrieve(id=chat.user_id)
    await MailService().send_new_video_email(user.email, coursechapter.name, new_video.name)
    await session.commit()


async def prepare_send_video(email: str, coursechapter_id: int):
    async with get_session_context() as session:
        await send_video(email, coursechapter_id, session)


@celery_app.task
def send_video_task(email: str, coursechapter_id: int) -> None:
    asyncio.run(prepare_send_video(email, coursechapter_id))


async def send_video_all() -> None:
    from src.services.chat import ChatService
    from src.services.course_chapter import CourseChapterService
    from src.services.mail import MailService
    from src.services.message import MessageService
    from src.services.user import UserService
    from src.services.video import VideoService

    async with get_session_context() as session:
        coursechapter_service = CourseChapterService(CourseChapterRepository(session))
        chat_service = ChatService(ChatRepository(session))
        user_service = UserService(UserRepository(session))
        video_service = VideoService(VideoRepository(session))
        message_service = MessageService(MessageRepository(session))

        time = datetime.strptime(str(datetime.now().hour), "%H").time()
        chat_list = await chat_service.list(receive_time=time, is_active=True)
        for chat in chat_list:
            user = await user_service.retrieve(id=chat.user_id)
            try:
                await user_service.check_subscription(user)
            except HasNoSubscriptionException:
                continue

            new_video = await video_service.list(coursechapter_id=chat.coursechapter_id, order=chat.last_video + 1)
            if new_video:
                new_video = new_video[0]
            else:
                continue

            await message_service.create(
                Message(
                    datetime=datetime.now(),
                    content=f"{new_video.name}\n{new_video.description}",
                    content_type=DataType.TEXT,
                    chat_id=chat.id,
                    theme_id=new_video.theme_id,
                )
            )
            await message_service.create(
                Message(
                    datetime=datetime.now(),
                    content=new_video.link,
                    content_type=DataType.VIDEO,
                    chat_id=chat.id,
                    theme_id=new_video.theme_id,
                )
            )
            await chat_service.update(id=chat.id, data=Chat(last_video=chat.last_video + 1))
            coursechapter = await coursechapter_service.retrieve(id=chat.coursechapter_id)
            await MailService().send_new_video_email(user.email, coursechapter.name, new_video.name)
        session.commit()


@celery_app.task
def send_video_all_task() -> None:
    asyncio.run(send_video_all())


async def check_subscription_end() -> None:
    date = datetime.now().date()
    from src.services.message import MessageService
    from src.services.user import UserService

    async with get_session_context() as session:
        user_service = UserService(UserRepository(session))
        message_service = MessageService(MessageRepository(session))

        users_without_subscription = await user_service.list(end_of_subscription=date)
        for user in users_without_subscription:
            await user_service.update(id=user.id, data=UpdateUser(subscription_type=SubscriptionType.NO_SUBSCRIPTION))
            await message_service.create(
                Message(
                    datetime=datetime.now(),
                    content=f"Ку, {user.fullname}.<br>" + SUBSCRIPTION_END_MESSAGE,
                    content_type=DataType.TEXT,
                    chat_id=(await user_service.get_base_chat(user.id)).id,
                )
            )
        session.commit()


@celery_app.task
def check_subscription_end_task() -> None:
    asyncio.run(check_subscription_end())


async def check_subscription_last_day() -> None:
    from src.services.message import MessageService
    from src.services.user import UserService

    async with get_session_context() as session:
        user_service = UserService(UserRepository(session))
        message_service = MessageService(MessageRepository(session))

        tomorrow = datetime.now().date() + timedelta(days=1)
        users = await user_service.list(end_of_subscription=tomorrow)
        for user in users:
            await message_service.create(
                Message(
                    datetime=datetime.now(),
                    content=SUBSCRIPTION_LAST_DAY_MESSAGE,
                    content_type=DataType.TEXT,
                    chat_id=(await user_service.get_base_chat(user.id)).id,
                )
            )
        session.commit()


@celery_app.task
def check_subscription_last_day_task() -> None:
    asyncio.run(check_subscription_last_day())


async def create_admin() -> None:
    from src.services.user import UserService

    async with get_session_context() as session:
        user_service = UserService(UserRepository(session))

        try:
            user = await user_service.create(
                AuthUser(
                    email=settings.admin_email,
                    password=settings.admin_password,
                )
            )
            await user_service.init_user(user)
            await user_service.update(user.id, data=AuthUser(is_active=True, is_admin=True))
        except IntegrityError:
            pass
        session.commit()


@celery_app.task
def create_admin_task() -> None:
    asyncio.run(create_admin())


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    sender.add_periodic_task(
        crontab(hour="0", minute="30", day_of_week="*"),
        sync_kinescope_task,
    )
    sender.add_periodic_task(
        crontab(hour="*", minute="0", day_of_week="1-5"),
        send_video_all_task,
    )
    sender.add_periodic_task(
        crontab(hour="10", minute="0", day_of_month="*"),
        check_subscription_end_task,
    )
    sender.add_periodic_task(
        crontab(hour="10", minute="0", day_of_month="*"),
        check_subscription_last_day_task,
    )
