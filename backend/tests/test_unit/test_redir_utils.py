import string

from src.modules.redir.utils import redir_random_url


class TestRedirRandomUrl:
    def test_returns_string(self):
        result = redir_random_url()
        assert isinstance(result, str)

    def test_length_is_7(self):
        result = redir_random_url()
        assert len(result) == 7

    def test_only_alphanumeric(self):
        valid = set(string.ascii_letters + string.digits)
        for _ in range(100):
            result = redir_random_url()
            assert all(c in valid for c in result)

    def test_generates_unique_values(self):
        results = {redir_random_url() for _ in range(50)}
        assert len(results) > 1
