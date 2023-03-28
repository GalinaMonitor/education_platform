from datetime import time
from typing import List, Optional

from sqlmodel import SQLModel

from db.models import CourseChapter


class CourseRead(SQLModel):
    id: int
    description: str
    name: str
    coursechapters: List[CourseChapter]
    receive_time: time


class CreateUser(SQLModel):
    email: str
    password: Optional[str]
    fullname: Optional[str]
    company: Optional[str]
    job: Optional[str]


class UpdateUser(SQLModel):
    fullname: Optional[str]
    company: Optional[str]
    job: Optional[str]
    avatar: Optional[str]


class UpdateChat(SQLModel):
    receive_time: time


class Time(SQLModel):
    time: str
