from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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


settings = Settings()
