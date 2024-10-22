from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


async def count_user_registered_last_seven_days(*, db: AsyncSession) -> int:
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_users_count = await db.scalar(
        select(func.count(User.id)).where(User.registration >= seven_days_ago)
    )
    return recent_users_count if recent_users_count else 0


async def top_five_users_with_longest_names(*, db: AsyncSession) -> list[str]:
    users = await db.scalars(
        select(User).order_by(func.length(User.username).desc(), User.username).limit(5)
    )
    usernames = [user.username for user in users.all()]
    return usernames


async def ratio_of_users_with_specific_domain(*, db: AsyncSession, domain: str) -> float:
    domain = domain.split("@")[-1]
    if domain:
        total_users_count = await db.scalar(select(func.count(User.id)))
        count_users_with_specific_domain = await db.scalar(
            select(func.count(User.id)).where(User.email.like(f"%{domain}"))
        )
        if total_users_count and count_users_with_specific_domain:
            return count_users_with_specific_domain / total_users_count
        return 0.0
    return 0.0
