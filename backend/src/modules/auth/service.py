from authx import TokenResponse
from src.core.exception import InvalidPassword, UserAlreadyExists, UserNotFound
from src.core.security import create_token, hashed_pass, verify_password
from src.modules.auth.repository import AuthRepository
from src.modules.auth.shemas import AuthRequestShema
from sqlalchemy.ext.asyncio import AsyncSession


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