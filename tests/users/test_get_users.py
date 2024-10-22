from httpx import AsyncClient

from src.users.schemas import UserFromDB


async def test_users_empty_list(async_client: AsyncClient) -> None:
    response = await async_client.get("/users/")
    json_response_data = response.json()

    assert response.status_code == 200
    assert len(json_response_data) == 0


async def test_users_list(async_client: AsyncClient, create_list_users) -> None:
    response = await async_client.get("/users/")
    json_response_data = response.json()

    assert response.status_code == 200
    assert len(json_response_data) == 25


async def test_user_detail(async_client: AsyncClient, create_list_users) -> None:
    user = create_list_users[0]
    response = await async_client.get("/users/1/")
    json_response_data = UserFromDB.model_validate(response.json())

    assert response.status_code == 200
    assert json_response_data.id == user.id
    assert json_response_data.username == user.username
    assert json_response_data.email == user.email
    assert json_response_data.registration == user.registration
