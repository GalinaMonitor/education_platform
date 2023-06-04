from datetime import date, datetime, time
from typing import List, Optional, Union

from pydantic import BaseModel as PydanticBaseModel

from db.models import DataType


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True


class Video(BaseModel):
    id: str
    order: int
    name: str
    link: str
    coursechapter_id: int
    theme_id: Optional[str]


class Theme(BaseModel):
    id: Optional[str]
    coursechapter_id: int
    name: str


class ThemeVideos(Theme):
    videos: List[Video] = []


class CourseChapter(BaseModel):
    id: Optional[int]
    description: Optional[str]
    name: Optional[str]
    kinescope_project_id: str
    course_id: int


class CourseChapterThemes(CourseChapter):
    themes: List[ThemeVideos] = []


class Course(BaseModel):
    id: Optional[int]
    description: Optional[str]
    name: Optional[str]
    color: Optional[str]


class CourseCourseChapters(Course):
    coursechapters: List[CourseChapter] = []


class CourseRead(Course):
    coursechapters: List[CourseChapterThemes]
    receive_time: Optional[time]
    is_active: bool


class User(BaseModel):
    id: int
    passed_welcome_page: bool
    time_on_platform: int
    avatar: str
    fullname: str
    company: str
    job: str
    email: str
    hashed_password: str
    has_subscription: bool
    end_of_subscription: Optional[date]


class AuthUser(BaseModel):
    email: str
    password: Optional[str]


class UpdateUser(BaseModel):
    fullname: Optional[str]
    company: Optional[str]
    job: Optional[str]
    passed_welcome_page: Optional[bool]
    time_on_platform: Optional[int]
    avatar: Optional[str]


class Message(BaseModel):
    id: Optional[int]
    datetime: datetime
    content: str
    content_type: DataType
    chat_id: int
    theme_id: Optional[str]


class Chat(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    receive_time: Optional[Union[time, datetime]]
    last_video: Optional[int]
    coursechapter_id: Optional[int]


class ChatMessages(Chat):
    messages: List[Message] = []


class UpdateChat(BaseModel):
    receive_time: time


class Time(BaseModel):
    time: str
