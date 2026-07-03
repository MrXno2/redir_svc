from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base_repo import BaseRepository
from src.db.models.user import UserModel


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