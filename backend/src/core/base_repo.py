from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def safe_commit(self, error_cls) -> bool:
        """Проверять на None результат выполнения."""
        try:
            await self.db.commit()
        except IntegrityError as err:
            await self.db.rollback()
            raise error_cls() from err
        return True
