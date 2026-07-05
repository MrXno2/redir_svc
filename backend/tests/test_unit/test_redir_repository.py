from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.redir import RedirModel
from src.modules.redir.repository import RedirRepository
from src.modules.redir.schemas import RedirResponseSchema


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def repo(mock_session):
    return RedirRepository(mock_session)


class TestRedirSetUrl:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_adds_redir_to_session(self, repo, mock_session):
        await repo.redir_set_url(
            user_uuid="user-1", def_url="https://example.com", redir_url="abc1234"
        )

        mock_session.add.assert_called_once()
        added = mock_session.add.call_args[0][0]
        assert isinstance(added, RedirModel)
        assert added.user_uuid == "user-1"
        assert added.default_url == "https://example.com"
        assert added.redir_url == "abc1234"

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_redir_model(self, repo):
        result = await repo.redir_set_url(
            user_uuid="u1", def_url="https://google.com", redir_url="xyz789"
        )
        assert isinstance(result, RedirModel)


class TestRedirGetList:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_list_of_schemas(self, repo, mock_session):
        mock_redir = RedirModel(
            user_uuid="user-1",
            default_url="https://example.com",
            redir_url="abc1234",
            redir_count=0,
        )
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_redir]
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.redir_get_list(user_uuid="user-1")

        assert len(result) == 1
        assert isinstance(result[0], RedirResponseSchema)
        assert result[0].default_url == "https://example.com"

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_empty_list(self, repo, mock_session):
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.redir_get_list(user_uuid="user-1")

        assert result == []


class TestRedirGetUrl:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_model_when_found(self, repo, mock_session):
        mock_redir = RedirModel(
            user_uuid="user-1",
            default_url="https://example.com",
            redir_url="abc1234",
            redir_count=5,
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_redir
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.redir_get_url(redir_url="abc1234")

        assert result == mock_redir
        assert result.redir_count == 5

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_none_when_not_found(self, repo, mock_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.redir_get_url(redir_url="nonexistent")

        assert result is None
