## Образовательная платформа
### Стек
- React, Antd, TailwindCSS
- FastAPI, SQLAlchemy, Celery, Alembic
- PostgreSQL, Redis
### Интеграции и фичи
- S3
- Kinescope API
- Sentry
- Панель администратора
### Запуск 
1. Создать .env на примере шаблона example.env
2. `docker compose -f docker-compose-local.yml up --build -d`
3. Можно создать аккаунт администратора с помощью команды `make task c=create_admin_task`

### TODO
- Тесты
- Разделение фронта и бэка
- Логирование задач celery
- Нормальная настройка structlog