from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str = "local-development-secret-change-me"
    database_url: str = "sqlite:///./aspireos.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:5173"
    access_token_minutes: int = 30
    digest_timezone: str = "Asia/Kolkata"
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

