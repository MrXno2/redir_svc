from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import UserModel
from src.modules.auth.repository import AuthRepository


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_session):
    return AuthRepository(mock_session)


class TestAuthRepositorySetUser:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_adds_user_to_session(self, repo, mock_session):
        await repo.set_user(login="testuser", pass_hash="hashedpwd")

        mock_session.add.assert_called_once()
        added_user = mock_session.add.call_args[0][0]
        assert isinstance(added_user, UserModel)
        assert added_user.login == "testuser"
        assert added_user.password_hash == "hashedpwd"

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_user_model(self, repo):
        result = await repo.set_user(login="john", pass_hash="hash123")
        assert isinstance(result, UserModel)
        assert result.login == "john"


class TestAuthRepositoryGetUser:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_user_when_found(self, repo, mock_session):
        mock_user = UserModel(login="testuser", password_hash="hash")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_user(login="testuser")

        assert result == mock_user

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_none_when_not_found(self, repo, mock_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_user(login="nonexistent")

        assert result is None
