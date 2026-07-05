from authx import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.core.exception import InvalidPassword, UserAlreadyExists, UserNotFound
from src.core.security import create_token, hashed_pass, verify_password
from src.modules.auth.repository import AuthRepository
from src.modules.auth.schemas import AuthRegisterShema, AuthLoginShema


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = AuthRepository(db)


    async def auth_login(self, req_data: AuthLoginShema) -> TokenResponse:
        user_model = await self.user_repo.get_user(login=req_data.login)
        if not user_model:
            raise UserNotFound()
        if verify_password(req_data.password, user_model.password_hash):
            return create_token(str(user_model.uuid))
        else:
            raise InvalidPassword()


    async def auth_register(self, req_data: AuthRegisterShema) -> TokenResponse | None:
        try:
            user_model = await self.user_repo.set_user(
                login=req_data.login, pass_hash=hashed_pass(req_data.password1)
            )
            await self.db.commit()
            return create_token(str(user_model.uuid))
        except IntegrityError as err:
            await self.db.rollback()
            raise UserAlreadyExists() from err
