from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    redis_url: str
    secret_key: str
    front_url: str
    kinescope_api_key: str


settings = Settings()
