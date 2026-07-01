from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.models import Base
from src.core.session import engine
from src.core.middleware import set_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("START redir_svc/backend")
    yield
    print("STOP redir_svc/backend")

app = FastAPI(lifespan=lifespan)

set_cors(app=app)