"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user import UserService
from app.services.group import GroupService
from app.api.routers.chat import ChatService


async def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)


async def get_group_service(db: AsyncSession = Depends(get_db)):
    return GroupService(db)


"""
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.auth.routers import AuthService
from src.db.session import get_db


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)
"""