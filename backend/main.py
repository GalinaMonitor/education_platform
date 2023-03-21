from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from api.authentication import router as authentication_router
from api.chat import router as chat_router
from api.course import router as course_router
from api.course_chapter import router as course_chapter_router
from db.config import engine
from db.models.all_models import *
from db.services.chat import ChatService
from db.services.course import CourseService
from db.services.course_chapter import CourseChapterService
from db.services.message import MessageService
from db.services.theme import ThemeService
from db.services.user import UserService
from settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.front_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication_router, prefix='/auth')
app.include_router(chat_router, prefix='/chat')
app.include_router(course_router, prefix='/course')
app.include_router(course_chapter_router, prefix='/course_chapter')

add_pagination(app)

async def init_data():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )
    async with async_session() as session:
        user = await UserService(session).create(CreateUser(
            email='test@test.com',
            password='secret'
        ))
        user = await UserService(session).update(id=user.id, data=User(fullname='Test test', has_subscription=True,
                                                                       end_of_subscription=datetime.now().date()))
        course = await CourseService(session).create(Course(
            name='Test Course'
        ))
        course_chapter = await CourseChapterService(session).create(CourseChapter(
            name='Test',
            course_id=course.id
        ))
        theme = await ThemeService(session).create(Theme(
            name='Test theme',
            course_chapter_id=course_chapter.id
        ))
        chat = await ChatService(session).create(Chat(
            user_id=user.id,
            coursechapter_id=course_chapter.id
        ))
        for i in range(50):
            message = await MessageService(session).create(Message(
                datetime=datetime.now(),
                content=f'Test text content {i}',
                content_type=0,
                chat_id=chat.id,
                theme_id=theme.id
            ))
        message = await MessageService(session).create(Message(
            datetime=datetime.now(),
            content='https://kinescope.io/202555445',
            content_type=1,
            chat_id=chat.id,
            theme_id=theme.id
        ))


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    await init_data()
