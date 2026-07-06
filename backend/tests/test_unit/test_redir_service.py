from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from src.core.exception import ListEmpty, RedirCreateError
from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema
from src.modules.redir.service import RedirService


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def service(mock_session):
    return RedirService(mock_session)


class TestRedirSetUrl:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_default_url_generates_random(self, service):
        req = RedirRequestSchema(
            default_url="https://example.com", custom_url="default"
        )
        mock_redir = MagicMock()
        mock_redir.default_url = "https://example.com"
        mock_redir.redir_url = "random7"
        mock_redir.redir_count = 0
        service.redir_repo.redir_set_url = AsyncMock(return_value=mock_redir)

        with patch(
            "src.modules.redir.service.redir_random_url", return_value="random7"
        ):
            result = await service.redir_set_url(user_uuid="u1", req_data=req)

        service.redir_repo.redir_set_url.assert_awaited_once_with(
            user_uuid="u1", def_url="https://example.com", redir_url="random7"
        )
        assert isinstance(result, RedirResponseSchema)

    @pytest.mark.asyncio(loop_scope="function")
    async def test_custom_url_used_directly(self, service):
        req = RedirRequestSchema(
            default_url="https://example.com", custom_url="myalias"
        )
        mock_redir = MagicMock()
        mock_redir.default_url = "https://example.com"
        mock_redir.redir_url = "myalias"
        mock_redir.redir_count = 0
        service.redir_repo.redir_set_url = AsyncMock(return_value=mock_redir)

        await service.redir_set_url(user_uuid="u1", req_data=req)

        service.redir_repo.redir_set_url.assert_awaited_once_with(
            user_uuid="u1", def_url="https://example.com", redir_url="myalias"
        )

    @pytest.mark.asyncio(loop_scope="function")
    async def test_integrity_error_custom_url_raises(self, service):
        req = RedirRequestSchema(default_url="https://example.com", custom_url="taken")
        service.redir_repo.redir_set_url = AsyncMock(
            side_effect=IntegrityError("test", "test", Exception())
        )

        with pytest.raises(RedirCreateError):
            await service.redir_set_url(user_uuid="u1", req_data=req)

    @pytest.mark.asyncio(loop_scope="function")
    async def test_integrity_error_default_url_retries_5_times(self, service):
        req = RedirRequestSchema(
            default_url="https://example.com", custom_url="default"
        )
        service.redir_repo.redir_set_url = AsyncMock(
            side_effect=IntegrityError("test", "test", Exception())
        )

        with patch("src.modules.redir.service.redir_random_url", return_value="rand"):
            with pytest.raises(RedirCreateError):
                await service.redir_set_url(user_uuid="u1", req_data=req)

            assert service.redir_repo.redir_set_url.call_count == 5


class TestRedirGetList:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_list(self, service):
        items = [
            RedirResponseSchema(
                default_url="https://a.com", redir_url="abc", redir_count=0
            )
        ]
        service.redir_repo.redir_get_list = AsyncMock(return_value=items)

        result = await service.redir_get_list(user_uuid="u1")

        assert result == items

    @pytest.mark.asyncio(loop_scope="function")
    async def test_raises_list_empty(self, service):
        service.redir_repo.redir_get_list = AsyncMock(return_value=[])

        with pytest.raises(ListEmpty):
            await service.redir_get_list(user_uuid="u1")


class TestRedirGetUrl:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_default_url(self, service):
        mock_redir = MagicMock()
        mock_redir.default_url = "https://target.com"
        service.redir_repo.redir_get_url = AsyncMock(return_value=mock_redir)
        service.redir_cache = AsyncMock()
        service.redir_cache.get.return_value = None

        result = await service.redir_get_url(redir_url="abc1234")

        assert result == "https://target.com"
        service.db.commit.assert_awaited_once()

    @pytest.mark.asyncio(loop_scope="function")
    async def test_returns_none_when_not_found(self, service):
        service.redir_repo.redir_get_url = AsyncMock(return_value=None)
        service.redir_cache = AsyncMock()
        service.redir_cache.get.return_value = None

        result = await service.redir_get_url(redir_url="nonexistent")

        assert result is None
