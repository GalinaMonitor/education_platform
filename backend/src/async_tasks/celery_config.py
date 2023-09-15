import asyncio
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.exc import IntegrityError

from src.exceptions import NotFoundException
from src.kinescope.api import KinescopeClient
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
from src.services.chat import ChatService
from src.services.course_chapter import CourseChapterService
from src.services.mail import MailService
from src.services.message import MessageService
from src.services.theme import ThemeService
from src.services.user import UserService
from src.services.video import VideoService
from src.settings import settings
from src.text_constants import EMAIL_NEW_VIDEO

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
    course_chapters = await CourseChapterService().list()
    for course_chapter in course_chapters:
        if not course_chapter.kinescope_project_id:
            continue
        video_list = KinescopeClient().get_project_video_list(course_chapter.kinescope_project_id)
        for video in video_list:
            if video.folder_id:
                try:
                    theme = await ThemeService().retrieve(id=video.folder_id)
                except NotFoundException:
                    theme = await ThemeService().create(
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
                db_video = await VideoService().retrieve(id=video.id)
                await VideoService().update(
                    id=db_video.id,
                    data=Video(
                        id=db_video.id,
                        order=order,
                        name=video.title,
                        link=video.play_link,
                        coursechapter_id=course_chapter.id,
                        theme_id=theme.id if theme else None,
                    ),
                )
            except NotFoundException:
                await VideoService().create(
                    data=Video(
                        id=video.id,
                        order=order,
                        name=video.title,
                        link=video.play_link,
                        coursechapter_id=course_chapter.id,
                        theme_id=theme.id if theme else None,
                    )
                )


@celery_app.task
def sync_kinescope_task() -> None:
    asyncio.run(sync_kinescope())


async def send_video(email: str, coursechapter_id: int) -> None:
    from src.main import email_conf

    user = await UserService().get_by_email(email)
    chat = await ChatService().get_or_create_from_user_and_chapter(user_id=user.id, coursechapter_id=coursechapter_id)
    new_video = await VideoService().list(coursechapter_id=chat.coursechapter_id, order=chat.last_video + 1)
    if new_video:
        new_video = new_video[0]
    else:
        return
    await MessageService().create(
        Message(
            datetime=datetime.now(),
            content=new_video.link,
            content_type=DataType.VIDEO,
            chat_id=chat.id,
            theme_id=new_video.theme_id,
        )
    )
    await MessageService().create(
        Message(
            datetime=datetime.now(),
            content=new_video.name,
            content_type=DataType.TEXT,
            chat_id=chat.id,
            theme_id=new_video.theme_id,
        )
    )
    await ChatService().update(id=chat.id, data=Chat(last_video=chat.last_video + 1))
    coursechapter = await CourseChapterService().retrieve(id=chat.coursechapter_id)
    user = await UserService().retrieve(id=chat.user_id)
    message = MessageSchema(
        subject=EMAIL_NEW_VIDEO,
        recipients=[user.email],
        template_body={
            "url": f"{settings.front_url}",
            "coursechapter": coursechapter.name,
            "video": new_video.name,
        },
        subtype=MessageType.html,
    )
    fm = FastMail(email_conf)
    await fm.send_message(message, template_name="new_video.html")


@celery_app.task
def send_video_task(email: str, coursechapter_id: int) -> None:
    asyncio.run(send_video(email, coursechapter_id))


async def send_video_all() -> None:
    time = datetime.strptime(str(datetime.now().hour), "%H").time()
    chat_list = await ChatService().list(receive_time=time, is_active=True)
    for chat in chat_list:
        new_video = await VideoService().list(coursechapter_id=chat.coursechapter_id, order=chat.last_video + 1)
        if new_video:
            new_video = new_video[0]
        else:
            continue
        await MessageService().create(
            Message(
                datetime=datetime.now(),
                content=new_video.link,
                content_type=DataType.VIDEO,
                chat_id=chat.id,
                theme_id=new_video.theme_id,
            )
        )
        await MessageService().create(
            Message(
                datetime=datetime.now(),
                content=new_video.name,
                content_type=DataType.TEXT,
                chat_id=chat.id,
                theme_id=new_video.theme_id,
            )
        )
        await ChatService().update(id=chat.id, data=Chat(last_video=chat.last_video + 1))
        coursechapter = await CourseChapterService().retrieve(id=chat.coursechapter_id)
        user = await UserService().retrieve(id=chat.user_id)
        await MailService().send_new_video_email(user.email, coursechapter.name, new_video.name)


@celery_app.task
def send_video_all_task() -> None:
    asyncio.run(send_video_all())


async def check_subscription() -> None:
    date = datetime.now().date()
    users_without_subscription = await UserService().list(end_of_subscription=date)
    for user in users_without_subscription:
        await UserService().update(id=user.id, data=UpdateUser(subscription_type=SubscriptionType.NO_SUBSCRIPTION))


@celery_app.task
def check_subscription_task() -> None:
    asyncio.run(check_subscription())


async def create_admin() -> None:
    try:
        user = await UserService().create(
            AuthUser(
                email=settings.admin_email,
                password=settings.admin_password,
            )
        )
        await UserService().init_user(user)
        await UserService().update(user.id, data=AuthUser(is_active=True, is_admin=True))
    except IntegrityError:
        pass


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
        crontab(hour="0", minute="0", day_of_month="*"),
        check_subscription_task,
    )
