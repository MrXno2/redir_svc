import pytest
from pydantic import ValidationError

from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema


class TestRedirRequestSchema:
    def test_adds_https_if_missing(self):
        schema = RedirRequestSchema(default_url="example.com")
        assert schema.default_url == "https://example.com"

    def test_keeps_http(self):
        schema = RedirRequestSchema(default_url="http://example.com")
        assert schema.default_url == "http://example.com"

    def test_keeps_https(self):
        schema = RedirRequestSchema(default_url="https://example.com")
        assert schema.default_url == "https://example.com"

    def test_empty_string_passes_through(self):
        schema = RedirRequestSchema(default_url="")
        assert schema.default_url == ""

    def test_default_custom_url(self):
        schema = RedirRequestSchema(default_url="https://example.com")
        assert schema.custom_url == "default"

    def test_custom_url_set(self):
        schema = RedirRequestSchema(default_url="https://example.com", custom_url="myalias")
        assert schema.custom_url == "myalias"

    def test_max_length_validation(self):
        with pytest.raises(ValidationError):
            RedirRequestSchema(default_url="x" * 256)

    def test_max_length_custom_url(self):
        with pytest.raises(ValidationError):
            RedirRequestSchema(default_url="ok", custom_url="x" * 256)


class TestRedirResponseSchema:
    def test_from_attributes(self):
        mock_obj = type("Mock", (), {
            "default_url": "https://example.com",
            "redir_url": "abc1234",
            "redir_count": 5,
        })()
        schema = RedirResponseSchema.model_validate(mock_obj)
        assert schema.default_url == "https://example.com"
        assert schema.redir_url == "abc1234"
        assert schema.redir_count == 5
