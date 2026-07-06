import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import settings
from src.db.base import Base
from src.db.session import get_db
from src.main import app


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(
        settings.POSTGRES_URL
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client):
    """Авторизованный клиент с токеном в cookie."""  # noqa: RUF002
    # Регистрация
    await client.post(
        "/api/auth/register",
        json={
            "login": "testuser",
            "password1": "password",
            "password2": "password",
        },
    )

    # Логин
    response = await client.post(
        "/api/auth/login",
        json={
            "login": "testuser",
            "password": "password",
        },
    )
    assert response.status_code == 200, "Login failed in fixture"

    token = response.json()["access_token"]
    client.cookies.set("access_token", token)

    yield client


@pytest_asyncio.fixture
async def client_with_redir(auth_client):
    """Авторизованный клиент с уже созданным редиректом."""  # noqa: RUF002
    response = await auth_client.post(
        "/api/redir/add",
        json={"default_url": "https://example.com", "custom_url": "qwerty"},
    )
    assert response.status_code == 200, "Redir creation failed in fixture"

    yield auth_client
