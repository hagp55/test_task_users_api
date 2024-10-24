from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


async def count_user_registered_last_seven_days(*, db: AsyncSession) -> int:
    """
    Asynchronously counts the number of users registered in the last seven days.

    Args:
        db (AsyncSession): An asynchronous session for the database.

    Returns:
        int: The number of users registered in the last seven days.
        If no users were registered, returns 0.
    """
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_users_count = await db.scalar(
        select(func.count(User.id)).where(User.registration >= seven_days_ago)
    )
    return recent_users_count if recent_users_count else 0


async def top_five_users_with_longest_names(*, db: AsyncSession) -> list[str]:
    """
    Asynchronously retrieves the usernames of the top five users with the longest names.

    Args:
        db (AsyncSession): An asynchronous session for the database.

    Returns:
        list[str]: A list of usernames of the top five users with the longest names.
    """
    users = await db.scalars(
        select(User).order_by(func.length(User.username).desc(), User.username).limit(5)
    )
    usernames = [user.username for user in users.all()]
    return usernames


async def percentage_users_with_specific_domain(*, db: AsyncSession, domain: str | None) -> str:
    """
    Asynchronously calculates the percentage of users with the specified domain
        in their email address.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        domain (str): The domain to filter users by.

    Returns:
        str: The percentage of users with the specified domain in their email address,
        or "0%" if no users were found.
    """
    if domain is not None:
        total_users_count = await db.scalar(select(func.count(User.id)))
        count_users_with_specific_domain = await db.scalar(
            select(func.count(User.id)).where(User.email.like(f"%@{domain}"))
        )
        if total_users_count and count_users_with_specific_domain:
            return f"{round(count_users_with_specific_domain / total_users_count * 100, 2)}%"
    return "0%"
