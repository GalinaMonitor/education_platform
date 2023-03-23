from datetime import time
from typing import List

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
    password: str


class UpdateChat(SQLModel):
    receive_time: time


class Time(SQLModel):
    time: str
