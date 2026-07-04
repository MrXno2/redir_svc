from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_repo import BaseRepository
from src.db.models.redir import RedirModel
from src.modules.redir.schemas import RedirResponseSchema


class RedirRepository(BaseRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)


    async def redir_set_url(
        self, user_uuid: str, def_url: str, redir_url: str
    ) -> RedirModel:
        url = RedirModel(user_uuid=user_uuid, default_url=def_url, redir_url=redir_url)
        self.db.add(url)
        return url


    async def redir_get_list(self, user_uuid: str) -> list[RedirResponseSchema]:
        redir_list = await self.db.execute(
            select(RedirModel).where(RedirModel.user_uuid == user_uuid)
        )
        redir_models = redir_list.scalars().all()

        return [RedirResponseSchema.model_validate(model) for model in redir_models]


    async def redir_get_url(self, redir_url: str) -> RedirModel | None:
        url = await self.db.execute(
            update(RedirModel)
            .where(RedirModel.redir_url == redir_url)
            .values(redir_count=RedirModel.redir_count + 1)
            .returning(RedirModel)
        )
        return url.scalar_one_or_none()
