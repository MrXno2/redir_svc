from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.modules.auth.service import AuthService
from src.modules.redir.service import RedirService

DbDep = Annotated[AsyncSession, Depends(get_db)]


async def get_redir_service(db: DbDep) -> RedirService:
    return RedirService(db)


RedirServiceDep = Annotated[RedirService, Depends(get_redir_service)]


async def get_auth_service(db: DbDep) -> AuthService:
    return AuthService(db)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
