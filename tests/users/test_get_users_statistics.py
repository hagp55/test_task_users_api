import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    argnames="domain,count_users,ratio",
    argvalues=[
        ("example.com", 20, 0.52),
        ("gmail.com", 20, 0.28),
        ("yandex.ru", 20, 0.2),
        ("mail.ru", 20, 0.0),
        ("", 20, 0.0),
    ],
)
async def test_users_statistics(
    async_client: AsyncClient, create_list_users, domain: str, count_users: int, ratio: float
) -> None:
    response = await async_client.get(f"/users/statistics/?domain={domain}")
    json_response_data = response.json()
    username_list = [user.username for user in create_list_users]
    sorted_username_list = set(sorted(username_list, key=len, reverse=True)[:5])

    assert response.status_code == 200
    assert json_response_data["count_users_registered_seven_days_ago"] == count_users
    assert json_response_data["ratio_of_users_with_specific_domain"] == ratio
    assert sorted_username_list == set(json_response_data["top_five_users_with_longest_names"])
