import bcrypt
from authx import AuthX, AuthXConfig, TokenResponse

from src.core.settings import settings

config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ACCESS_COOKIE_NAME=settings.JWT_ACCESS_COOKIE_NAME,
    JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_COOKIE_NAME=settings.JWT_REFRESH_COOKIE_NAME,
    JWT_REFRESH_TOKEN_EXPIRES=settings.JWT_REFRESH_TOKEN_EXPIRES,
    JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION,
    JWT_COOKIE_CSRF_PROTECT=settings.JWT_COOKIE_CSRF_PROTECT,
)

auth = AuthX(config=config)


# функция которая принимает id юзера и делает из него JWT токены
def create_token(id_user: str) -> TokenResponse:
    access_token = auth.create_access_token(uid=id_user)
    refresh_token = auth.create_refresh_token(uid=id_user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# хэширует пароль
def hashed_pass(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # ← возвращаем строку


# проверка пароля
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),  # ← превращаем строку в байты
    )
