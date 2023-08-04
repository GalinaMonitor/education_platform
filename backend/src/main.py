from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import ConnectionConfig
from fastapi_pagination import add_pagination

from src.admin.config import admin
from src.api.authentication import router as authentication_router
from src.api.chat import router as chat_router
from src.api.course import router as course_router
from src.api.course_chapter import router as course_chapter_router
from src.api.user import router as user_router

# from src.middlewares import LoggerMiddleware
from src.settings import settings

# app = FastAPI(openapi_url=None)
app = FastAPI()
admin.mount_to(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.front_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(LoggerMiddleware)

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT=465,
    MAIL_SERVER=settings.mail_server,
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
