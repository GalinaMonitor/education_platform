import asyncio
from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from src.db.config import async_session
from src.db.models import DataType, SubscriptionType
from src.db.services.chat import ChatService
from src.db.services.course_chapter import CourseChapterService
from src.db.services.message import MessageService
from src.db.services.theme import ThemeService
from src.db.services.user import UserService
from src.db.services.video import VideoService
from src.exceptions import NotFoundException
from src.kinescope.api import KinescopeClient
from src.models import Chat, Message, Theme, UpdateUser, User, Video
from src.settings import settings

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
)


async def sync_kinescope():
    async with async_session() as session:
        course_chapters = await CourseChapterService(session).list()
        for course_chapter in course_chapters:
            video_list = KinescopeClient().get_project_video_list(course_chapter.kinescope_project_id)
            for video in video_list:
                try:
                    await VideoService(session).retrieve(id=video.id)
                except NotFoundException:
                    if video.folder_id:
                        try:
                            theme = await ThemeService(session).retrieve(id=video.folder_id)
                        except NotFoundException:
                            theme = await ThemeService(session).create(
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
                    await VideoService(session).create(
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
def sync_kinescope_task():
    asyncio.run(sync_kinescope())


async def send_video():
    async with async_session() as session:
        time = datetime.strptime(str(datetime.now().hour), "%H").time()
        chat_list = await ChatService(session).list(receive_time=time)
        for chat in chat_list:
            new_video = await VideoService(session).list(
                coursechapter_id=chat.coursechapter_id, order=chat.last_video + 1
            )
            if new_video:
                new_video = new_video[0]
            else:
                continue
            await MessageService(session).create(
                Message(
                    datetime=datetime.now(),
                    content=new_video.link,
                    content_type=DataType.VIDEO,
                    chat_id=chat.id,
                    theme_id=new_video.theme_id,
                )
            )
            await MessageService(session).create(
                Message(
                    datetime=datetime.now(),
                    content=new_video.name,
                    content_type=DataType.TEXT,
                    chat_id=chat.id,
                    theme_id=new_video.theme_id,
                )
            )
            await ChatService(session).update(id=chat.id, data=Chat(last_video=chat.last_video + 1))


@celery_app.task
def send_video_task():
    asyncio.run(send_video())


async def check_subscription():
    date = datetime.now().date()
    async with async_session() as session:
        users_without_subscription = await UserService(session).list(end_of_subscription=date)
        for user in users_without_subscription:
            await UserService(session).update(
                id=user.id, data=UpdateUser(subscription_type=SubscriptionType.NO_SUBSCRIPTION)
            )


@celery_app.task
def check_subscription_task():
    asyncio.run(check_subscription())


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="0", minute="30", day_of_week="*"),
        sync_kinescope_task,
    )
    sender.add_periodic_task(
        crontab(hour="*", minute="0", day_of_week="1-5"),
        send_video_task,
    )
    sender.add_periodic_task(
        crontab(hour="0", minute="0", day_of_month="*"),
        check_subscription_task,
    )
