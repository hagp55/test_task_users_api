import pytest
from httpx import AsyncClient

from src.users.schemas import UserFromDB


async def test_successfully_update_user(async_client: AsyncClient, create_list_users) -> None:
    user = create_list_users[0]
    response = await async_client.get(f"/users/{user.id}/")
    new_data = {"username": "new_username", "email": "newemail@example.com"}
    response = await async_client.put(f"/users/{user.id}/", json=new_data)
    json_response_data = UserFromDB.model_validate(response.json())

    assert response.status_code == 200
    assert json_response_data.username == new_data["username"]
    assert json_response_data.email == new_data["email"]


async def test_not_successfully_update_not_exist_user(async_client: AsyncClient) -> None:
    new_data = {"username": "new_username", "email": "newemail@example.com"}
    response = await async_client.put("/users/1/", json=new_data)

    assert response.status_code == 404


@pytest.mark.parametrize(
    argnames="username,email",
    argvalues=[
        (None, "user@example.com"),
        ("user", None),
        ("user", ""),
        ("", "user@example.com"),
    ],
)
async def test_not_successfully_create_user_with_no_valid_inputs(
    async_client: AsyncClient, username: str, email: str, create_list_users
) -> None:
    user = create_list_users[0]
    new_data = {"username": username, "email": email}
    response = await async_client.put(f"/users/{user.id}/", json=new_data)

    assert response.status_code == 422
