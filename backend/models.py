from datetime import date, datetime, time
from typing import List, Optional, Union

from pydantic import BaseModel as PydanticBaseModel

from db.models import DataType, SubscriptionType


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


class ThemeRead(Theme):
    video_amount: Optional[int]
    viewed_video_amount: Optional[int]


class CourseChapter(BaseModel):
    id: Optional[int]
    description: Optional[str]
    name: Optional[str]
    kinescope_project_id: str
    course_id: int


class CourseChapterRead(CourseChapter):
    messages_amount: Optional[int]


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
    coursechapters: List[CourseChapter] = []
    course_chapter_id: Optional[int]
    receive_time: Optional[time]
    is_active: Optional[bool]


class User(BaseModel):
    id: int
    is_admin: bool
    passed_welcome_page: bool
    time_on_platform: int
    avatar: str
    fullname: str
    company: str
    job: str
    email: str
    hashed_password: str
    subscription_type: SubscriptionType
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
    subscription_type: Optional[SubscriptionType]
    end_of_subscription: Optional[date]


class Message(BaseModel):
    id: Optional[int]
    datetime: Optional[datetime]
    content: Optional[str]
    content_type: Optional[DataType]
    chat_id: Optional[int]
    is_read: Optional[bool]
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
