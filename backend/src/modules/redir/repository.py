from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.redir import RedirModel


class RedirRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def redir_set_url(
        self, user_uuid: str, def_url: str, redir_url: str
    ) -> RedirModel:
        url = RedirModel(user_uuid=user_uuid, default_url=def_url, redir_url=redir_url)
        self.db.add(url)
        return url

    async def redir_get_list(self, user_uuid: str) -> list[RedirModel]:
        redir_list = await self.db.execute(
            select(RedirModel).where(RedirModel.user_uuid == user_uuid)
        )
        return list(redir_list.scalars().all())

    async def redir_get_url(self, redir_url: str) -> RedirModel | None:
        url = await self.db.execute(
            update(RedirModel)
            .where(RedirModel.redir_url == redir_url)
            .values(redir_count=RedirModel.redir_count + 1)
            .returning(RedirModel)
        )
        return url.scalar_one_or_none()

    async def redir_del_url(self, uuid_user: str, redir_url: str) -> None:
        await self.db.execute(
            delete(RedirModel).where(
                (RedirModel.user_uuid == uuid_user)
                & (RedirModel.redir_url == redir_url)
            )
        )
        await self.db.commit()
