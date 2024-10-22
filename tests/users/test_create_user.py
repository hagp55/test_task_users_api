import pytest
from httpx import AsyncClient


async def test_successfully_create_user(async_client: AsyncClient) -> None:
    data = {"username": "user", "email": "user@example.com"}
    response = await async_client.post("/users/", json=data)
    json_response_data = response.json()

    assert response.status_code == 201
    assert json_response_data["username"] == "user"
    assert json_response_data["email"] == "user@example.com"


async def test_not_successfully_create_user_exits_username(async_client: AsyncClient) -> None:
    data = {"username": "user", "email": "user@example.com"}
    response = await async_client.post("/users/", json=data)
    response = await async_client.post("/users/", json=data)
    json_response_data = response.json()

    assert response.status_code == 400
    assert json_response_data == {
        "detail": f"User with username: {data['username']} already exists"
    }


async def test_not_successfully_create_user_exits_email(async_client: AsyncClient) -> None:
    data = {"username": "user1", "email": "user@example.com"}
    response = await async_client.post("/users/", json=data)

    data = {"username": "user2", "email": "user@example.com"}
    response = await async_client.post("/users/", json=data)
    json_response_data = response.json()

    assert response.status_code == 400
    assert json_response_data == {"detail": f"User with email: {data['email']} already exists"}


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
    async_client: AsyncClient, username: str, email: str
) -> None:
    data = {"username": username, "email": email}
    response = await async_client.post("/users/", json=data)

    assert response.status_code == 422
