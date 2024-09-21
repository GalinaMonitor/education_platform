from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin, ModelView

from src.admin.auth_provider import MyAuthProvider
from src.db.config import engine
from src.db.models import Chat, Course, CourseChapter, Message, Theme, User, Video
from src.settings import settings

admin = Admin(
    engine,
    title="Ку-помогу",
    i18n_config=I18nConfig(default_locale="ru"),
    auth_provider=MyAuthProvider(allow_paths=["/statics/logo.svg"]),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.secret_key)],
)


class UserView(ModelView):
    fields = [
        "is_admin",
        "is_active",
        "passed_welcome_page",
        "time_on_platform",
        "avatar",
        "fullname",
        "company",
        "job",
        "email",
        "end_of_subscription",
        "subscription_type",
        "service_uuid",
    ]
    exclude_fields_from_list = ["chats"]


class ChatView(ModelView):
    fields = [
        "user_id",
        "receive_time",
        "is_active",
        "last_video",
        "get_welcome_message",
        "coursechapter_id",
        "coursechapter",
        "chat_type",
    ]
    exclude_fields_from_list = ["messages"]


class CourseChapterView(ModelView):
    fields = [
        "description",
        "name",
        "kinescope_project_id",
        "course_id",
        "welcome_message",
        "mentor_id",
        "mentor",
    ]
    exclude_fields_from_list = ["chats"]


class ThemeView(ModelView):
    fields = ["coursechapter_id", "name"]
    exclude_fields_from_list = ["messages"]


class MessageView(ModelView):
    fields = [
        "datetime",
        "content",
        "content_type",
        "is_read",
        "chat_id",
        "theme_id",
        "theme",
    ]


class VideoView(ModelView):
    fields = [
        "id",
        "order",
        "name",
        "link",
        "description",
        "coursechapter_id",
        "theme_id",
        "theme",
    ]


admin.add_view(ModelView(Course, label="Курс"))
admin.add_view(UserView(User, label="Пользователи"))
admin.add_view(ChatView(Chat, label="Чаты"))
admin.add_view(CourseChapterView(CourseChapter, label="Уровни курсов"))
admin.add_view(ThemeView(Theme, label="Темы"))
admin.add_view(MessageView(Message, label="Сообщения"))
admin.add_view(VideoView(Video, label="Видео"))
