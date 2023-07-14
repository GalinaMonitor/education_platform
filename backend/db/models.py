import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, backref, relationship, sessionmaker
from starlette.requests import Request

from db.config import engine


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, default=None)
    receive_time = Column(TIME, default=datetime.strptime("10:00", "%H:%M"))
    is_active = Column(Boolean, default=False)
    last_video = Column(Integer, default=0)
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    messages = relationship("Message", backref=backref("chat"))
    coursechapter = relationship("CourseChapter", backref=backref("chats"))

    async def __admin_repr__(self, request: Request):
        async_session = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        async with async_session() as session:
            from db.services.course_chapter import CourseChapterService
            from db.services.user import UserService

            chat_repr = []
            if self.coursechapter_id:
                chat_repr.append((await CourseChapterService(session).retrieve(self.coursechapter_id)).name)
            if self.user_id:
                chat_repr.append((await UserService(session).retrieve(self.user_id)).email)
            return " ".join(chat_repr)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    is_admin = Column(Boolean, default=False)
    passed_welcome_page = Column(Boolean, default=False)
    time_on_platform = Column(Integer, default=0)
    avatar = Column(Text, default="")
    fullname = Column(Text, default="")
    company = Column(Text, default="")
    job = Column(Text, default="")
    email = Column(Text, default="", unique=True)
    hashed_password = Column(Text)
    has_subscription = Column(Boolean, default=False)
    end_of_subscription = Column(Date, default=None)
    chats = relationship(Chat, backref=backref("user"))

    async def __admin_repr__(self, request: Request):
        return self.email


class CourseChapter(Base):
    __tablename__ = "coursechapter"

    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Text, default="")
    name = Column(Text, default="")
    kinescope_project_id = Column(Text, default="")
    course_id = Column(Integer, ForeignKey("course.id"), nullable=True, default=None)
    themes = relationship("Theme", backref=backref("coursechapter"))

    async def __admin_repr__(self, request: Request):
        return self.name


class DataType(str, enum.Enum):
    TEXT = "TEXT"
    VIDEO = "VIDEO"


class Theme(Base):
    __tablename__ = "theme"

    id = Column(Text, primary_key=True)
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    name = Column(Text, default="")
    videos = relationship("Video", back_populates="theme")
    messages = relationship("Message", back_populates="theme")

    async def __admin_repr__(self, request: Request):
        return self.name


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, autoincrement=True, primary_key=True)
    datetime = Column(DateTime)
    content = Column(Text, default="")
    content_type = Column(Enum(DataType))
    is_read = Column(Boolean, default=False)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=True, default=None)
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="messages")

    async def __admin_repr__(self, request: Request):
        return f"{self.content}"


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Text, default="")
    name = Column(Text, default="")
    color = Column(Text, default="#ff7d1f")
    coursechapters = relationship(CourseChapter, backref=backref("course"), order_by=CourseChapter.id)

    async def __admin_repr__(self, request: Request):
        return self.name


class Video(Base):
    __tablename__ = "video"

    id = Column(Text, primary_key=True, default=None)
    order = Column(Integer, default="")
    name = Column(Text, default="")
    link = Column(Text, default="")
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="videos")
