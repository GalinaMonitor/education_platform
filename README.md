## Образовательная платформа
### Стек
- React, Antd, TailwindCSS длля фронта
- FastAPI, SQLAlchemy, Celery, Alembic для бека
- PostgreSQL, Redis бд
- K8s, Vault и Helm для деплоя
### Интеграции и фичи
- S3
- Kinescope API
- Sentry
- Панель администратора
### Запуск 
1. Создать .env на примере шаблона example.env
2. `docker compose -f docker-compose-local.yml up --build -d`
3. Можно создать аккаунт администратора с помощью команды `make task c=create_admin_task`
