from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@db:5432/brivo")
    jwt_secret: str = Field(default="change-me-in-env")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
