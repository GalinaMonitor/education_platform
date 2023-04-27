from flask_admin.contrib.sqla import ModelView


class CourseChapterView(ModelView):
    form_columns = ["id", "description", "name", "kinescope_project_id"]
    column_list = ["id", "description", "name", "kinescope_project_id"]

    column_labels = {
        "id": "id",
        "name": "Название",
        "description": "Описание",
        "kinescope_project_id": "ID проекта в Kinescope",
    }
