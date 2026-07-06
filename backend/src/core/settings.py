from datetime import timedelta
from pathlib import Path

from authx.types import TokenLocation
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# нужно установить прямой путь к корню проекта и передавать в env
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )

    PROJECT_NAME: str = "my-project"
    # docker run -d --name my-redis -p 6379:6379 redis:alpine
    REDIS_HOST: str = "localhost"
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
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

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
