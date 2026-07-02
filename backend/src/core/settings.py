from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    POSTGRES_URL: str # "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"

    PROJECT_NAME: str = "my-project"
    
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    JWT_SECRET_KEY: str # "very_secret_key"
    JWT_ACCESS_COOKIE_NAME: str = "access_token"
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600
    JWT_REFRESH_COOKIE_NAME: str = "refresh_token"
    JWT_REFRESH_TOKEN_EXPIRES: int = 604800
    JWT_TOKEN_LOCATION: list[str] = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT: bool = False


settings = Settings()