import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.orm import DeclarativeBase, backref, relationship


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, default=None)
    receive_time = Column(TIME, default=datetime.strptime("10:00", "%H:%M"))
    last_video = Column(Integer, default=0)
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    messages = relationship("Message", backref=backref("chat"))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    avatar = Column(Text, default="")
    fullname = Column(Text, default="")
    company = Column(Text, default="")
    job = Column(Text, default="")
    email = Column(Text, default="", unique=True)
    hashed_password = Column(Text)
    has_subscription = Column(Boolean, default=False)
    end_of_subscription = Column(Date, default=None)


class CourseChapter(Base):
    __tablename__ = "coursechapter"

    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Text, default="")
    name = Column(Text, default="")
    kinescope_project_id = Column(Text, default="")
    color = Column(Text, default="#ff7d1f")
    course_id = Column(Integer, ForeignKey("course.id"), nullable=True, default=None)
    themes = relationship("Theme", backref=backref("coursechapter"))


class DataType(int, enum.Enum):
    TEXT = 0
    VIDEO = 1


class Theme(Base):
    __tablename__ = "theme"

    id = Column(Text, primary_key=True)
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    name = Column(Text, default="")
    videos = relationship("Video", back_populates="theme")
    messages = relationship("Message", back_populates="theme")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, autoincrement=True, primary_key=True)
    datetime = Column(DateTime)
    content = Column(Text, default="")
    content_type = Column(Enum(DataType))
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=True, default=None)
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="messages")


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Text, default="")
    name = Column(Text, default="")
    coursechapters = relationship(CourseChapter, backref=backref("course"))


class Video(Base):
    __tablename__ = "video"

    id = Column(Text, primary_key=True, default=None)
    order = Column(Integer, default="")
    name = Column(Text, default="")
    link = Column(Text, default="")
    coursechapter_id = Column(Integer, ForeignKey("coursechapter.id"), nullable=True, default=None)
    theme_id = Column(Text, ForeignKey("theme.id"), nullable=True, default=None)
    theme = relationship(Theme, back_populates="videos")
