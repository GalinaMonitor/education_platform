from datetime import date, datetime, time
from typing import List, Optional, Union
from uuid import UUID

from pydantic import NaiveDatetime
from pydantic.config import ConfigDict
from pydantic.main import BaseModel as PydanticBaseModel

from src.db.models import DataType, SubscriptionType


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)


class Video(BaseModel):
    id: str
    order: int
    name: str
    link: str
    coursechapter_id: int
    theme_id: Optional[str] = None


class Theme(BaseModel):
    id: Optional[str] = None
    coursechapter_id: int
    name: str


class ThemeVideos(Theme):
    videos: List[Video] = []


class ThemeRead(Theme):
    video_amount: Optional[int] = None
    viewed_video_amount: Optional[int] = None


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
    service_uuid: Optional[UUID] = None
    subscription_type: SubscriptionType
    end_of_subscription: Optional[date] = None
    is_active: Optional[bool] = None


class UserAvatar(BaseModel):
    id: int
    avatar: str
    fullname: str
    email: str


class CourseChapter(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    name: Optional[str] = None
    kinescope_project_id: str
    course_id: int
    welcome_message: Optional[str] = None


class CourseChapterMentor(CourseChapter):
    mentor: Optional[UserAvatar] = None


class CourseChapterRead(CourseChapterMentor):
    messages_amount: Optional[int] = None


class CourseChapterThemes(CourseChapter):
    themes: List[ThemeVideos] = []


class Course(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None


class CourseCourseChapters(Course):
    coursechapters: List[CourseChapter] = []


class CourseRead(Course):
    coursechapters: List[CourseChapter] = []
    course_chapter_id: Optional[int] = None
    receive_time: Optional[time] = None
    is_active: Optional[bool] = None


class AuthUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    hashed_password: Optional[str] = None
    service_uuid: Optional[UUID] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UpdateUser(BaseModel):
    fullname: Optional[str] = None
    company: Optional[str] = None
    job: Optional[str] = None
    passed_welcome_page: Optional[bool] = None
    time_on_platform: Optional[int] = None
    avatar: Optional[str] = None
    subscription_type: Optional[SubscriptionType] = None
    end_of_subscription: Optional[date] = None


class Message(BaseModel):
    id: Optional[int] = None
    datetime: Optional[NaiveDatetime] = None
    content: Optional[str] = None
    content_type: Optional[DataType] = None
    chat_id: Optional[int] = None
    is_read: Optional[bool] = None
    theme_id: Optional[str] = None


class Chat(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    receive_time: Optional[Union[time, datetime]] = None
    last_video: Optional[int] = None
    coursechapter_id: Optional[int] = None
    get_welcome_message: Optional[bool] = None


class ChatMessages(Chat):
    messages: List[Message] = []


class UpdateChat(BaseModel):
    receive_time: Optional[time] = None
    get_welcome_message: Optional[bool] = None


class Time(BaseModel):
    time: str
