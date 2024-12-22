import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.orm import DeclarativeBase, backref, relationship
from starlette.requests import Request

from src.schemas import ChatType, DataType, SubscriptionType


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)


class Chat(Base):
    __tablename__ = "chat"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, default=None)
    receive_time = Column(TIME, default=datetime.strptime("10:00", "%H:%M"))
    is_active = Column(Boolean, default=False)
    last_video = Column(Integer, default=0)
    get_welcome_message = Column(Boolean, default=False)
    coursechapter_id = Column(
        Integer, ForeignKey("coursechapter.id"), nullable=True, default=None
    )
    chat_type = Column(Enum(ChatType), default=ChatType.COURSE)
    messages = relationship("Message", backref=backref("chat"), cascade="all, delete")
    coursechapter = relationship("CourseChapter", backref=backref("chats"))

    async def __admin_repr__(self, request: Request) -> str:
        from src.db.config import get_session_context
        from src.repositories.course_chapter import CourseChapterRepository
        from src.repositories.user import UserRepository
        from src.services.course_chapter import CourseChapterService
        from src.services.user import UserService

        chat_repr = []
        async with get_session_context() as session:
            if self.coursechapter_id:
                chat_repr.append(
                    (
                        await CourseChapterService(
                            CourseChapterRepository(session)
                        ).retrieve(self.coursechapter_id)
                    ).name
                )
            if self.user_id:
                chat_repr.append(
                    (
                        await UserService(UserRepository(session)).retrieve(
                            self.user_id
                        )
                    ).email
                )
        return " ".join(chat_repr)


class User(Base):
    __tablename__ = "user"

    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    passed_welcome_page = Column(Boolean, default=False)
    time_on_platform = Column(Integer, default=0)
    avatar = Column(Text, default="")
    fullname = Column(Text, default="")
    company = Column(Text, default="")
    job = Column(Text, default="")
    email = Column(Text, default="", unique=True)
    hashed_password = Column(Text)
    end_of_subscription = Column(Date, default=None)
    subscription_type = Column(Enum(SubscriptionType))
    service_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    chats = relationship(Chat, backref=backref("user"), cascade="all, delete")

    async def __admin_repr__(self, request: Request) -> str:
        return self.email


class CourseChapter(Base):
    __tablename__ = "coursechapter"

    description = Column(Text, default="")
    name = Column(Text, default="")
    kinescope_project_id = Column(Text, default="")
    course_id = Column(Integer, ForeignKey("course.id"), nullable=True, default=None)
    mentor_id = Column(Integer, ForeignKey("user.id"), nullable=True, default=None)
    welcome_message = Column(Text, default="")
    mentor = relationship("User", backref=backref("coursechapter"))
    themes = relationship(
        "Theme", backref=backref("coursechapter"), cascade="all, delete"
    )

    async def __admin_repr__(self, request: Request):
        return self.name


class Theme(Base):
    __tablename__ = "theme"

    id = Column(Text, primary_key=True)
    coursechapter_id = Column(
        Integer, ForeignKey("coursechapter.id"), nullable=True, default=None
    )
    name = Column(Text, default="")
    videos = relationship("Video", back_populates="theme", cascade="all, delete")
    messages = relationship("Message", back_populates="theme", cascade="all, delete")

    async def __admin_repr__(self, request: Request):
        return self.name


class Message(Base):
    __tablename__ = "message"

    datetime = Column(DateTime)
    content = Column(Text, default="")
    content_type = Column(Enum(DataType))
    is_read = Column(Boolean, default=False)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=True, default=None)
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="messages")

    async def __admin_repr__(self, request: Request) -> str:
        return f"{self.content}"


class Course(Base):
    __tablename__ = "course"

    description = Column(Text, default="")
    name = Column(Text, default="")
    color = Column(Text, default="#ff3300")
    coursechapters = relationship(
        CourseChapter,
        backref=backref("course"),
        order_by=CourseChapter.id,
        cascade="all, delete",
    )

    async def __admin_repr__(self, request: Request):
        return self.name


class Video(Base):
    __tablename__ = "video"

    id = Column(Text, primary_key=True, default=None)
    order = Column(Integer, default="")
    name = Column(Text, default="")
    link = Column(Text, default="")
    description = Column(Text, default="")
    coursechapter_id = Column(
        Integer, ForeignKey("coursechapter.id"), nullable=True, default=None
    )
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="videos")

    async def __admin_repr__(self, request: Request):
        return self.name
