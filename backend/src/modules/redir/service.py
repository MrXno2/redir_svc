from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exception import ListEmpty, RedirCreateError, URLNotFound
from src.modules.redir.repository import RedirRepository
from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema
from src.modules.redir.utils import redir_random_url


class RedirService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.redir_repo = RedirRepository(db)

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
            return redir_list
        else:
            raise ListEmpty()

    async def redir_get_url(self, redir_url: str) -> str:
        def_url = await self.redir_repo.redir_get_url(redir_url=redir_url)
        await self.redir_repo.safe_commit(URLNotFound)
        if def_url is not None:
            return def_url.default_url
        else:
            raise URLNotFound()
