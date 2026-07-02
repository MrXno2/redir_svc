from authx import TokenResponse
from fastapi import APIRouter, Depends, Response
from typing import Any
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.db.session import get_db
from src.core.exception import InvalidPassword, UserAlreadyExists, UserNotFound
from src.core.security import create_token, hashed_pass, verify_password
from src.core.base_repo import BaseRepository
from src.db.models.user import UserModel



async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)



class AuthRequestShema(BaseModel):
    login: str = Field(min_length=4, pattern=r'^[a-zA-Z0-9]+$', description="От 4 символов, только a-z A-Z 0-9.")
    password1: str = Field(min_length=6, pattern=r'^\S+$', description="От 6 символов, без пробелов.")
    password2: str = Field(min_length=6, pattern=r'^\S+$', description="От 6 символов, без пробелов.")

    @field_validator('login')
    @classmethod
    def validator_login(cls, v: Any):
        return v # убрать

    @model_validator(mode='after')
    def check_password(self):
        if self.password1 != self.password2:
            raise ValueError("Пароли не совпадают.")
        return self



class AuthRepository(BaseRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def set_user(self, login: str, pass_hash: str) -> UserModel:
        new_user = UserModel(
            login = login,
            password_hash = pass_hash
        )
        self.db.add(new_user)
        return new_user

    async def get_user(self, login: str) -> UserModel:
        user = await self.db.execute(
            select(UserModel)
            .where(UserModel.login == login)
            .limit(1)
        )
        return user.scalar_one_or_none()


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = AuthRepository(db)

    async def auth_login(self, req_data: AuthRequestShema) -> TokenResponse:
        user_model = await self.user_repo.get_user(login=req_data.login)
        if not user_model:
            raise UserNotFound()
        if verify_password(req_data.password1, user_model.password_hash):
            return create_token(user_model.uuid)
        else:
            raise InvalidPassword()

    async def auth_register(self, req_data: AuthRequestShema) -> TokenResponse:
        user_model = await self.user_repo.set_user(login=req_data.login, pass_hash=hashed_pass(req_data.password1))
        is_commit = await self.user_repo.safe_commit(UserAlreadyExists)
        if is_commit:
            return create_token(user_model.uuid)
    

router = APIRouter(prefix="/api/auth")



@router.post("/login")
async def login_user(
    req_data: AuthRequestShema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token = await auth_service.auth_login(req_data=req_data)
    response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
    response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
    return token

@router.post("/register")
async def register_user(
    req_data: AuthRequestShema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token = await auth_service.auth_register(req_data=req_data)
    response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
    response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
    return token