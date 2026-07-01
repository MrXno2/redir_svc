from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "my-project"
    
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    POSTGRES_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"

    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]


settings = Settings()