import pytest
from httpx import AsyncClient

from src.users.models import User
from src.users.schemas import UserFromDB


async def test_users_empty_list(async_client: AsyncClient) -> None:
    response = await async_client.get("/users/")
    json_response_data = response.json()

    assert response.status_code == 200
    assert len(json_response_data) == 0


async def test_users_list(async_client: AsyncClient, create_list_users: tuple[User, ...]) -> None:
    response = await async_client.get("/users/")
    json_response_data = response.json()

    assert response.status_code == 200
    assert len(json_response_data) == 25


@pytest.mark.parametrize(
    "page, size, expected_count_users",
    [
        (1, 10, 10),
        (1, 3, 3),
        (2, 8, 8),
        (8, 2, 2),
        (100, 25, 0),
        (52, 100, 0),
    ],
)
async def test_users_list_with_paginate(
    async_client: AsyncClient,
    create_list_users: tuple[User, ...],
    page: int,
    size: int,
    expected_count_users: int,
) -> None:
    response = await async_client.get(f"/users/?page={page}&size={size}")
    json_response_data = response.json()
    users_list = [
        UserFromDB.model_validate(user)
        for user in create_list_users[(page - 1) * size : size * page]
    ]
    user_list_response = [UserFromDB.model_validate(user) for user in json_response_data]

    assert response.status_code == 200
    assert user_list_response == users_list
    assert len(json_response_data) == expected_count_users


@pytest.mark.parametrize(
    "page, size",
    [
        (0, 2),
        (-2, 10),
    ],
)
async def test_not_successfully_users_list_with_paginate(
    async_client: AsyncClient, create_list_users: tuple[User, ...], page: int, size: int
) -> None:
    response = await async_client.get(f"/users/?page={page}&size={size}")

    assert response.status_code == 422


async def test_user_detail(async_client: AsyncClient, create_list_users: tuple[User, ...]) -> None:
    user = create_list_users[0]
    response = await async_client.get("/users/1/")
    json_response_data = UserFromDB.model_validate(response.json())

    assert response.status_code == 200
    assert json_response_data.id == user.id
    assert json_response_data.username == user.username
    assert json_response_data.email == user.email
    assert json_response_data.registration == user.registration
