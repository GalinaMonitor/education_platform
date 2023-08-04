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
admin.add_view(ModelView(Course, label="Курс"))
admin.add_view(ModelView(User, label="Пользователи"))
admin.add_view(ModelView(Chat, label="Чаты"))
admin.add_view(ModelView(CourseChapter, label="Уровни курсов"))
admin.add_view(ModelView(Theme, label="Темы"))
admin.add_view(ModelView(Message, label="Сообщения"))
admin.add_view(ModelView(Video, label="Видео"))
