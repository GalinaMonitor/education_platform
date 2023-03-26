from datetime import time, datetime, date
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, Integer, func
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import SQLModel, Field, Relationship, select


class Chat(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
    user_id: Optional[int] = Field(foreign_key='user.id', nullable=True, default=None)
    receive_time: time = Field(sa_column=Column(TIME, default=datetime.strptime("10:00", "%H:%M")))
    last_video: int = Field(default=0)
    coursechapter_id: Optional[int] = Field(foreign_key='coursechapter.id', nullable=True, default=None)
    messages: List['Message'] = Relationship(back_populates='chat')


class User(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
    fullname: str = Field(default='')
    company: str = Field(default='')
    job: str = Field(default='')
    email: str = Field(unique=True)
    hashed_password: str
    has_subscription: bool = Field(default=False)
    end_of_subscription: Optional[date] = Field(default=None)


class CourseChapter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default='')
    name: str
    kinescope_project_id: str = Field(default='')
    course_id: Optional[int] = Field(foreign_key='course.id', nullable=True, default=None)
    course: Optional['Course'] = Relationship(back_populates="coursechapters")


class DataType(int, Enum):
    TEXT = 0
    VIDEO = 1


class Theme(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, primary_key=True))
    course_chapter_id: Optional[int] = Field(foreign_key='coursechapter.id', nullable=True, default=None)
    name: str


class Message(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
    datetime: datetime
    content: str
    content_type: DataType
    chat_id: Optional[int] = Field(foreign_key='chat.id', nullable=True, default=None)
    theme_id: Optional[int] = Field(foreign_key='theme.id', nullable=True, default=None)
    chat: Optional['Chat'] = Relationship(back_populates='messages')


class Course(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default='')
    name: str
    coursechapters: List['CourseChapter'] = Relationship(back_populates="course")

    @declared_attr
    def receive_time(self):
        return column_property(
            select([func.max(Chat.receive_time)]).scalar_subquery()
        )


class Video(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    order: int
    name: str
    coursechapter_id: Optional[int] = Field(foreign_key='coursechapter.id', nullable=True, default=None)
