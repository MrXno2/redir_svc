import secrets
import string
from uuid import UUID
from src.core.exception import ListEmpty, URLNotFound
from src.core.security import auth
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.redir import RedirModel
from src.core.base_repo import BaseRepository
from src.db.session import get_db
from sqlalchemy.exc import IntegrityError



async def get_redir_service(db: AsyncSession = Depends(get_db)):
    return RedirService(db)


class RedirRequestSchema(BaseModel):
    default_url: str

    @field_validator("default_url", mode="before")
    @classmethod
    def add_default_url(cls, v: str) -> str:
        if not v:
            return v
        if v.startswith(("http://", "https://")):
            return v
        return f"https://{v}"
    

class RedirListResponseSchema(BaseModel):
    uuid: UUID
    user_uuid: UUID
    default_url: str
    redir_url: str
    redir_count: int


class RedirRepository(BaseRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def redir_set_url(self, user_uuid: str, def_url: str, redir_url: str) -> RedirModel:
        url = RedirModel(
            user_uuid = user_uuid,
            default_url = def_url,
            redir_url = redir_url
        )
        self.db.add(url)
        return url
    
    async def redir_get_list(self, user_uuid: str) -> list[RedirListResponseSchema]:
        redir_list = await self.db.execute(
            select(RedirModel)
            .where(RedirModel.user_uuid == user_uuid)
        )
        return redir_list.scalars().all()


    async def redir_get_url(self, redir_url: str) -> RedirModel:
        url = await self.db.execute(
            update(RedirModel)
            .where(RedirModel.redir_url == redir_url)
            .values(redir_count=RedirModel.redir_count + 1)
            .returning(RedirModel)
        )
        return url.scalar_one_or_none()


class RedirService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.redir_repo = RedirRepository(db)

    async def redir_set_url(self, user_uuid: str, def_url: str) -> None:
        for _ in range(5):
            try:
                random_url = redir_random_url()
                await self.redir_repo.redir_set_url(
                    user_uuid=user_uuid,
                    def_url=def_url,
                    redir_url=random_url
                )
                await self.db.commit()
                return
            except IntegrityError:
                await self.db.rollback()
                """Тут еще попытка"""

    async def redir_get_list(self, user_uuid: str) -> list[RedirListResponseSchema]:
        redir_list = await self.redir_repo.redir_get_list(user_uuid=user_uuid)
        if redir_list:
            return redir_list
        else:
            raise ListEmpty()

    async def redir_get_url(self, redir_url: str) -> str:
        def_url = await self.redir_repo.redir_get_url(redir_url=redir_url)
        await self.redir_repo.safe_commit(URLNotFound())
        if def_url is not None:
            return def_url.default_url
        else:
            raise URLNotFound()
        


router_api = APIRouter(prefix="/api/redir")

@router_api.post("/add")
async def redir_set_url(
    req_data: RedirRequestSchema,
    redir_service: RedirService = Depends(get_redir_service),
    payload = Depends(auth.access_token_required)
) -> None:
    user_uuid = payload.sub
    await redir_service.redir_set_url(
        def_url=req_data.default_url, 
        user_uuid=user_uuid
    )

@router_api.get("/list")
async def redir_get_list(
    redir_service: RedirService = Depends(get_redir_service),
    payload = Depends(auth.access_token_required)
) -> list[RedirListResponseSchema]:
    user_uuid = payload.sub
    return await redir_service.redir_get_list(user_uuid=user_uuid)


router_redir = APIRouter(prefix="")


@router_redir.get("/{redir_url}")
async def redir_in_url(
    redir_url: str,
    redir_service: RedirService = Depends(get_redir_service)
) -> str:
    new_url = await redir_service.redir_get_url(redir_url=redir_url)
    if new_url:
        return RedirectResponse(url=new_url, status_code=302)


def redir_random_url():
    chars = string.ascii_letters + string.digits
    short_code = ''.join(secrets.choice(chars) for _ in range(7))
    return short_code