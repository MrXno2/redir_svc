import pytest


@pytest.mark.asyncio(loop_scope="function")
async def test_redir_add(auth_client):
    response = await auth_client.post(
        "/api/redir/add", json={"default_url": "qwerty.com", "custom_url": "default"}
    )
    data = response.json()
    if response.status_code == 200:
        assert data["default_url"] == "https://qwerty.com"
        assert data["redir_count"] == 0
        assert len(data["redir_url"]) == 7


@pytest.mark.asyncio(loop_scope="function")
async def test_redir_list(client_with_redir):
    response = await client_with_redir.get("/api/redir/list")
    data = response.json()
    if response.status_code == 200:
        assert "default_url" in data[0]
        assert "redir_url" in data[0]
        assert "redir_count" in data[0]


@pytest.mark.asyncio(loop_scope="function")
async def test_redir_in_url(client_with_redir):
    response = await client_with_redir.get("/go/qwerty", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"
