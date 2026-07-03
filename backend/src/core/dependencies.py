from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.service import AuthService
from src.db.session import get_db
from src.modules.redir.service import RedirService


async def get_redir_service(db: AsyncSession = Depends(get_db)):
    return RedirService(db)


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)