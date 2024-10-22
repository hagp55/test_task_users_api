from httpx import AsyncClient

from src.users.models import User


async def test_successfully_delete_user(
    async_client: AsyncClient, create_list_users: tuple[User, ...]
) -> None:
    response = await async_client.get("/users/")
    assert len(response.json()) == 25

    user = create_list_users[0]
    response = await async_client.delete(f"/users/{user.id}/")

    assert response.status_code == 204
    response = await async_client.get("/users/")
    assert len(response.json()) == 24


async def test_not_successfully_delete_user(async_client: AsyncClient) -> None:
    response = await async_client.delete("/users/1/")

    assert response.status_code == 404
    assert response.json() == {"detail": "User with id: 1 does not exist"}
