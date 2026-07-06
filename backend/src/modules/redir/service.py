from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache.redis import redir_cache_redis
from src.core.exception import ListEmpty, RedirCreateError, URLNotFound
from src.modules.redir.repository import RedirRepository
from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema
from src.modules.redir.utils import redir_random_url


class RedirService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.redir_repo = RedirRepository(db)
        self.redir_cache = redir_cache_redis  # редис

    async def redir_set_url(
        self, user_uuid: str, req_data: RedirRequestSchema
    ) -> RedirResponseSchema:
        for _ in range(5):
            try:
                if req_data.custom_url == "default":
                    url = redir_random_url()
                else:
                    url = req_data.custom_url

                new_url = await self.redir_repo.redir_set_url(
                    user_uuid=user_uuid, def_url=req_data.default_url, redir_url=url
                )
                await self.db.commit()
                return RedirResponseSchema.model_validate(new_url)
            except IntegrityError as err:
                await self.db.rollback()
                if req_data.custom_url != "default":
                    raise RedirCreateError() from err
        raise RedirCreateError()

    async def redir_get_list(self, user_uuid: str) -> list[RedirResponseSchema]:
        redir_list = await self.redir_repo.redir_get_list(user_uuid=user_uuid)
        if redir_list:
            return [RedirResponseSchema.model_validate(model) for model in redir_list]
        else:
            raise ListEmpty()

        # добавить запись в кеш после коммита

    async def redir_get_url(self, redir_url: str) -> str | None:
        cached_url = await self.redir_cache.get(redir_url)
        if cached_url:
            return cached_url
        try:
            def_url = await self.redir_repo.redir_get_url(redir_url=redir_url)
            await self.db.commit()
            if def_url is not None:
                await self.redir_cache.set(redir_url, def_url.default_url)
                return def_url.default_url
        except IntegrityError as err:
            await self.db.rollback()
            raise URLNotFound() from err

        # сделать инвалидацию кеша после коммита

    async def redir_del_url(self, user_uuid: str, redir_url: str) -> None:
        await self.redir_cache.delete(redir_url)
        await self.redir_repo.redir_del_url(uuid_user=user_uuid, redir_url=redir_url)
