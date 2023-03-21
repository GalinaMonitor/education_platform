from datetime import datetime, date
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field, Relationship


class Chat(SQLModel, table=True):
    id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
    user_id: Optional[int] = Field(foreign_key='user.id', nullable=True, default=None)
    coursechapter_id: Optional[int] = Field(foreign_key='coursechapter.id', nullable=True, default=None)
    messages: List['Message'] = Relationship(back_populates='chat')


class BaseUser(SQLModel):
    id: int = Field(sa_column=Column(Integer, autoincrement=True, primary_key=True))
    fullname: str = Field(default='')
    email: str = Field(unique=True)
    hashed_password: str
    has_subscription: bool = Field(default=False)
    end_of_subscription: Optional[date] = Field(default=None)


class User(BaseUser, table=True):
    pass


class CreateUser(SQLModel):
    email: str
    password: str


class CourseChapter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default='')
    name: str
    course_id: Optional[int] = Field(foreign_key='course.id', nullable=True, default=None)
    course: Optional['Course'] = Relationship(back_populates="coursechapters")


class CourseBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default='')
    name: str
    kinescope_project_id: str = Field(default='')


class Course(CourseBase, table=True):
    coursechapters: List[CourseChapter] = Relationship(back_populates="course")


class CourseRead(CourseBase):
    coursechapters: List[CourseChapter]


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
