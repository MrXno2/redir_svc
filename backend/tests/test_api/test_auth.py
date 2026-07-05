import pytest


@pytest.mark.asyncio(loop_scope="function")
async def test_auth_login(client):
    login_response = await client.post(
        "/api/auth/login",
        json={
            "login": "qwerty",
            "password": "qwerty"
        })
    data = login_response.json()

    if login_response.status_code == 404:
        assert data["error_type"] == "UserNotFound"
    elif login_response.status_code == 401:
        assert data["error_type"] == "InvalidPassword"
    elif login_response.status_code == 200:
        assert data["token_type"] == "bearer"
        assert "access_token" in data
    else:
        pytest.fail(f"Unexpected status code: {login_response.status_code}")
    
    


@pytest.mark.asyncio(loop_scope="function")
async def test_auth_register(client):
    register_response = await client.post(
        "/api/auth/register",
        json={
            "login": "qwerty1",
            "password1": "qwerty",
            "password2": "qwerty"
        }
    )
    data = register_response.json()

    if register_response.status_code == 409:
        assert data["error_type"] == "UserAlreadyExists"
    elif register_response.status_code == 200:
        assert data["token_type"] == "bearer"
        assert "access_token" in data