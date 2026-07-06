import pytest
from pydantic import ValidationError

from src.modules.auth.schemas import AuthLoginShema, AuthRegisterShema


class TestAuthRegisterSchema:
    def test_valid_data(self):
        schema = AuthRegisterShema(
            login="testuser", password1="pass123", password2="pass123"
        )
        assert schema.login == "testuser"
        assert schema.password1 == "pass123"

    def test_passwords_mismatch(self):
        with pytest.raises(ValidationError, match="Пароли не совпадают"):
            AuthRegisterShema(
                login="testuser", password1="pass123", password2="pass456"
            )

    def test_login_too_short(self):
        with pytest.raises(ValidationError):
            AuthRegisterShema(login="abc", password1="pass123", password2="pass123")

    def test_login_special_chars(self):
        with pytest.raises(ValidationError):
            AuthRegisterShema(
                login="test@user", password1="pass123", password2="pass123"
            )

    def test_login_with_underscores(self):
        with pytest.raises(ValidationError):
            AuthRegisterShema(
                login="test_user", password1="pass123", password2="pass123"
            )

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            AuthRegisterShema(login="testuser", password1="short", password2="short")

    def test_password_with_spaces(self):
        with pytest.raises(ValidationError):
            AuthRegisterShema(
                login="testuser", password1="pass word", password2="pass word"
            )


class TestAuthLoginSchema:
    def test_valid_data(self):
        schema = AuthLoginShema(login="testuser", password="pass123")
        assert schema.login == "testuser"
        assert schema.password == "pass123"

    def test_login_too_short(self):
        with pytest.raises(ValidationError):
            AuthLoginShema(login="abc", password="pass123")

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            AuthLoginShema(login="testuser", password="short")

    def test_login_special_chars(self):
        with pytest.raises(ValidationError):
            AuthLoginShema(login="test!user", password="pass123")
