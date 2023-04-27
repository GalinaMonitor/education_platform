from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    form_columns = [
        "id",
        "fullname",
        "company",
        "job",
        "email",
        "has_subscription",
        "end_of_subscription",
    ]
    column_list = [
        "id",
        "fullname",
        "company",
        "job",
        "email",
        "has_subscription",
        "end_of_subscription",
    ]
    column_searchable_list = ["fullname"]

    column_labels = {
        "id": "id",
        "fullname": "ФИО",
        "company": "Компания",
        "job": "Должность",
        "has_subscription": "Имеет подписку",
        "end_of_subscription": "Конец подписки",
    }
