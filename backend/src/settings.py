from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    db_url: str
    redis_url: str
    secret_key: str
    front_url: str
    kinescope_api_key: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str
    aws_host: str
    mail_username: str
    mail_password: str
    mail_server: str
    sentry_dsn: str
    admin_email: str
    admin_password: str
    lifepay_api_key: str
    lifepay_login: str
    service_url: str


settings = Settings()
