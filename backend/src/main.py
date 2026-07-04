from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logger import logger
from src.core.exception_handler import register_exception_handlers
from src.core.middleware import set_cors
from src.core.security import auth
from src.db.base import Base
from src.db.session import engine
from src.modules.auth.routers import router as router_auth
from src.modules.redir.routers import router_api, router_redir


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.warning("START redir_svc/backend")
    yield
    logger.warning("STOP redir_svc/backend")


app = FastAPI(lifespan=lifespan)

set_cors(app=app)

auth.handle_errors(app)

register_exception_handlers(app)

app.include_router(router_auth)

app.include_router(router_api)

app.include_router(router_redir)
