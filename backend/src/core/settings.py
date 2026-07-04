from datetime import timedelta

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from authx.types import TokenLocation


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "my-project"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    JWT_SECRET_KEY: str = "dopustim_pass"  # "very_secret_key"
    JWT_ACCESS_COOKIE_NAME: str = "access_token"
    JWT_ACCESS_TOKEN_EXPIRES_SECONDS: int = 3600
    JWT_REFRESH_COOKIE_NAME: str = "refresh_token"
    JWT_REFRESH_TOKEN_EXPIRES_SECONDS: int = 604800
    JWT_TOKEN_LOCATION: list[TokenLocation] = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT: bool = False

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_NAME: str = "postgres"
    POSTGRES_IP: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_IP}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    @computed_field
    @property
    def JWT_ACCESS_TOKEN_EXPIRES(self) -> timedelta:
        return timedelta(seconds=self.JWT_ACCESS_TOKEN_EXPIRES_SECONDS)

    @computed_field
    @property
    def JWT_REFRESH_TOKEN_EXPIRES(self) -> timedelta:
        return timedelta(seconds=self.JWT_REFRESH_TOKEN_EXPIRES_SECONDS)

settings = Settings()
