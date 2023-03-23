import asyncio
from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from db.config import async_session
from db.exceptions import NotFoundException
from db.models import Video, Message, DataType
from db.services.chat import ChatService
from db.services.course_chapter import CourseChapterService
from db.services.message import MessageService
from db.services.video import VideoService
from kinescope.api import KinescopeClient
from settings import settings

celery_app = Celery(
    broker=settings.redis_url,
    redis_max_connections=3,
    result_persistent=True,
    enable_ut=True,
    timezone="Europe/Moscow",
    redis_socket_timeout=15,
    event_serializer='json',
    task_serializer='json',
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
                    await VideoService(session).create(data=Video(
                        id=video.id,
                        order=int(video.title.split('. ')[0]),
                        name=video.title,
                        coursechapter_id=course_chapter.id
                    ))


@celery_app.task
def sync_kinescope_task():
    asyncio.run(sync_kinescope())


async def send_video():
    async with async_session() as session:
        time = datetime.strptime(str(datetime.now().hour), "%H").time()
        chat_list = await ChatService(session).list(receive_time=time)
        for chat in chat_list:
            new_video = await VideoService(session).list(coursechapter_id=chat.coursechapter_id,
                                                         order=chat.last_video + 1)
            await MessageService(session).create(Message(
                datetime=datetime.now(),
                content=new_video.name,
                content_type=DataType.VIDEO,
                chat_id=chat.id,
            ))


@celery_app.task
def send_video_task():
    asyncio.run(send_video())


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(
            hour='*',
            minute='0',
            day_of_week='1-5'
        ),
        send_video_task,
    )
    sender.add_periodic_task(
        crontab(
            hour='0',
            minute='0',
            day_of_week='1-5'
        ),
        sync_kinescope_task,
    )
