from flask import Flask, session
from flask.globals import request
from flask_admin import Admin
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy

from admin.views.course_chapter import CourseChapterView
from admin.views.user import UserView
from backend.db.models import CourseChapter, User

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
    if request.args.get("lang"):
        session["lang"] = request.args.get("lang")
    return session.get("lang", "ru")


app.config.from_prefixed_env()
db = SQLAlchemy(session_options={"autoflush": False})
db.init_app(app)

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(
    app,
    name="Ку-помогу",
    template_mode="bootstrap4",
)


admin.add_view(UserView(User, db.session, "Пользователи"))
admin.add_view(CourseChapterView(CourseChapter, db.session, "Курс"))
