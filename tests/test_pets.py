import pytest
from fastapi import status


async def get_auth_headers(client, username, password):
    await client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    response = await client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_pet(client):
    headers = await get_auth_headers(client, "petowner", "12345")

    payload = {"name": "Rex"}

    response = await client.post("/pets/create", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Rex"
    assert data["hunger"] == 100
    assert data["energy"] == 100


@pytest.mark.asyncio
async def test_get_pet_stats(client):
    headers = await get_auth_headers(client, "stats_user", "12345")

    create_res = await client.post(
        "/pets/create", json={"name": "Fluffy"}, headers=headers
    )
    pet_id = create_res.json()["id"]

    response = await client.get(f"/pets/{pet_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Fluffy"


@pytest.mark.asyncio
async def test_pet_action_feed(client):
    headers = await get_auth_headers(client, "feed_user", "12345")

    create_res = await client.post(
        "/pets/create", json={"name": "HungryBoy"}, headers=headers
    )
    pet_id = create_res.json()["id"]

    action_payload = {"type_stats": "hunger"}
    response = await client.patch(
        f"/pets/{pet_id}/action", json=action_payload, headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["hunger"] == 100

    history_res = await client.get(f"/pets/{pet_id}/actions_history", headers=headers)
    history = history_res.json()
    assert len(history) == 1
    assert history[0]["action_type"] == "feed"
