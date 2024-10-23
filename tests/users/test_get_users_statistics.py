import pytest
from httpx import AsyncClient

from src.users.models import User


@pytest.mark.parametrize(
    argnames="domain,count_users,ratio",
    argvalues=[
        ("example.com", 20, "52.0%"),
        ("gmail.com", 20, "28.0%"),
        ("yandex.ru", 20, "20.0%"),
        ("mail.ru", 20, "0%"),
    ],
)
async def test_users_statistics(
    async_client: AsyncClient,
    create_list_users: tuple[User, ...],
    domain: str,
    count_users: int,
    ratio: float,
) -> None:
    response = await async_client.get(f"/users/statistics/?domain={domain}")
    json_response_data = response.json()
    username_list = [user.username for user in create_list_users]
    sorted_username_list = set(sorted(username_list, key=lambda x: (-len(x), x))[:5])
    assert response.status_code == 200
    assert json_response_data["count_users_registered_seven_days_ago"] == count_users
    assert sorted_username_list == set(json_response_data["top_five_users_with_longest_names"])
    assert json_response_data["percent_of_users_with_specific_domain"] == ratio


async def test_users_statistics_with_empty_users(async_client: AsyncClient) -> None:
    response = await async_client.get("/users/statistics/?domain=example.com")
    json_response_data = response.json()
    assert response.status_code == 200
    assert json_response_data == {
        "count_users_registered_seven_days_ago": 0,
        "top_five_users_with_longest_names": [],
        "percent_of_users_with_specific_domain": "0%",
    }


async def test_users_statistics_with_empty_users_invalid_domain(async_client: AsyncClient) -> None:
    response = await async_client.get("/users/statistics/?domain=dggg")
    json_response_data = response.json()
    assert response.status_code == 422
    assert json_response_data["detail"][0]["type"] == "string_pattern_mismatch"
