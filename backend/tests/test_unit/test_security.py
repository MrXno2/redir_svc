from src.core.security import create_token, hashed_pass, verify_password


class TestHashedPass:
    def test_returns_string(self):
        result = hashed_pass("mypassword")
        assert isinstance(result, str)

    def test_different_hashes_for_same_password(self):
        h1 = hashed_pass("test")
        h2 = hashed_pass("test")
        assert h1 != h2

    def test_hash_not_equal_to_plain(self):
        result = hashed_pass("secret")
        assert result != "secret"


class TestVerifyPassword:
    def test_correct_password(self):
        hashed = hashed_pass("qwerty123")
        assert verify_password("qwerty123", hashed) is True

    def test_incorrect_password(self):
        hashed = hashed_pass("qwerty123")
        assert verify_password("wrongpassword", hashed) is False

    def test_empty_password(self):
        hashed = hashed_pass("")
        assert verify_password("", hashed) is True
        assert verify_password("notempty", hashed) is False


class TestCreateToken:
    def test_returns_token_response(self):
        token = create_token("user-uuid-123")
        assert hasattr(token, "access_token")
        assert hasattr(token, "refresh_token")

    def test_tokens_are_strings(self):
        token = create_token("user-uuid-123")
        assert isinstance(token.access_token, str)
        assert isinstance(token.refresh_token, str)

    def test_different_users_different_tokens(self):
        t1 = create_token("user-1")
        t2 = create_token("user-2")
        assert t1.access_token != t2.access_token
