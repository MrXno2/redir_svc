from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from src.core.exception import InvalidPassword, UserAlreadyExists, UserNotFound
from src.modules.auth.schemas import AuthLoginShema, AuthRegisterShema
from src.modules.auth.service import AuthService


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def service(mock_session):
    return AuthService(mock_session)


class TestAuthLogin:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_success(self, service):
        mock_user = MagicMock()
        mock_user.password_hash = "hashedpwd"
        mock_user.uuid = "user-uuid-123"
        service.user_repo.get_user = AsyncMock(return_value=mock_user)

        req = AuthLoginShema(login="testuser", password="mypassword")

        with (
            patch("src.modules.auth.service.verify_password", return_value=True),
            patch("src.modules.auth.service.create_token") as mock_create,
        ):
            mock_create.return_value = MagicMock(access_token="at", refresh_token="rt")
            result = await service.auth_login(req)

            service.user_repo.get_user.assert_awaited_once_with(login="testuser")
            mock_create.assert_called_once_with("user-uuid-123")
            assert result.access_token == "at"

    @pytest.mark.asyncio(loop_scope="function")
    async def test_user_not_found(self, service):
        service.user_repo.get_user = AsyncMock(return_value=None)
        req = AuthLoginShema(login="nobody", password="password")

        with pytest.raises(UserNotFound):
            await service.auth_login(req)

    @pytest.mark.asyncio(loop_scope="function")
    async def test_invalid_password(self, service):
        mock_user = MagicMock()
        mock_user.password_hash = "hashedpwd"
        service.user_repo.get_user = AsyncMock(return_value=mock_user)

        req = AuthLoginShema(login="testuser", password="wrongpassword")

        with (
            patch("src.modules.auth.service.verify_password", return_value=False),
            pytest.raises(InvalidPassword),
        ):
            await service.auth_login(req)


class TestAuthRegister:
    @pytest.mark.asyncio(loop_scope="function")
    async def test_success(self, service):
        mock_user = MagicMock()
        mock_user.uuid = "new-uuid"
        service.user_repo.set_user = AsyncMock(return_value=mock_user)

        req = AuthRegisterShema(
            login="newuser", password1="pass123", password2="pass123"
        )

        with (
            patch("src.modules.auth.service.hashed_pass", return_value="hashed"),
            patch("src.modules.auth.service.create_token") as mock_create,
        ):
            mock_create.return_value = MagicMock(access_token="at", refresh_token="rt")
            result = await service.auth_register(req)

            service.user_repo.set_user.assert_awaited_once_with(
                login="newuser", pass_hash="hashed"
            )
            service.db.commit.assert_awaited_once()
            assert result.access_token == "at"

    @pytest.mark.asyncio(loop_scope="function")
    async def test_duplicate_user(self, service):
        service.user_repo.set_user = AsyncMock(
            side_effect=IntegrityError("test", "test", Exception())
        )

        req = AuthRegisterShema(
            login="dupuser", password1="pass123", password2="pass123"
        )

        with (
            patch("src.modules.auth.service.hashed_pass", return_value="hashed"),
            pytest.raises(UserAlreadyExists),
        ):
            await service.auth_register(req)
