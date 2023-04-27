from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import ConnectionConfig
from fastapi_pagination import add_pagination

from backend.api.authentication import router as authentication_router
from backend.api.chat import router as chat_router
from backend.api.course import router as course_router
from backend.api.course_chapter import router as course_chapter_router
from backend.api.user import router as user_router
from backend.db.config import engine
from backend.db.models import Base
from backend.settings import settings
from backend.utils import init_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.front_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_FROM_NAME="Education platform",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

app.include_router(authentication_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")
app.include_router(course_router, prefix="/course")
app.include_router(course_chapter_router, prefix="/course_chapter")
app.include_router(user_router, prefix="/user")

add_pagination(app)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await init_data()
