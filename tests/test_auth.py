import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_register_user(client):
    payload = {"username": "testuser", "password": "securepassword123"}
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "pets" in data


@pytest.mark.asyncio
async def test_login_user(client):
    register_payload = {"username": "loginuser", "password": "mypassword"}
    await client.post("/auth/register", json=register_payload)

    login_data = {"username": "loginuser", "password": "mypassword"}
    response = await client.post("/auth/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
