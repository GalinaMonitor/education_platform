from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    secret_key: str


settings = Settings()
