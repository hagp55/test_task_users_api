from fastapi import HTTPException
from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate


async def get_user_by_id(*, db: AsyncSession, user_id: int) -> User:
    user = await db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} does not exist")
    return user


async def get_exists_user_by_username_or_email(
    *, db: AsyncSession, username: str, email: str
) -> None:
    exists_user = await db.scalar(
        select(User).where(or_(User.username == username, User.email == email))
    )
    if exists_user:
        raise HTTPException(status_code=400, detail="User with username or email already exists")


async def get_users(*, db: AsyncSession, skip: int, limit: int) -> list[User]:
    users = await db.scalars(select(User).offset(skip).limit(limit))
    return list(users.all())


async def create_user(*, db: AsyncSession, user_in: UserCreate) -> User:
    await get_exists_user_by_username_or_email(
        db=db, username=user_in.username, email=user_in.email
    )
    user = User(username=user_in.username, email=user_in.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(*, db: AsyncSession, user_in: UserUpdate, user_id: int) -> User:
    user = await get_user_by_id(db=db, user_id=user_id)
    await get_exists_user_by_username_or_email(
        db=db, username=user_in.username, email=user_in.email
    )
    await db.execute(update(User).where(User.id == user_id).values(user_in.model_dump()))
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(*, db: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(db=db, user_id=user_id)
    await db.delete(user)
    await db.commit()
