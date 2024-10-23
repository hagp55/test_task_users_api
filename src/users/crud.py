from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate


async def get_user_by_id(*, db: AsyncSession, user_id: int) -> User:
    """
    Asynchronously retrieves a user from the database by its id.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        user_id (int): The id of the user to retrieve.

    Returns:
        User: The User object with the specified id.

    Raises:
        HTTPException: If the user with the specified id does not exist,
        a 404 Not Found exception is raised.
    """
    user = await db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} does not exist"
        )
    return user


async def check_user_exists(*, db: AsyncSession, username: str, email: str) -> None:
    """
    Asynchronously checks if a user with the given username or email already exists in the database.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        username (str): The username to check for.
        email (str): The email to check for.

    Raises:
        HTTPException: If a user with the given username or email already exists,
            a 400 Bad Request exception is raised with an appropriate error message.
    """
    exists_user = await db.scalar(select(User).where(User.username == username))
    if exists_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username: {username} already exists",
        )
    exists_user = await db.scalar(select(User).where(User.email == email))
    if exists_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email: {email} already exists",
        )


async def get_users(*, db: AsyncSession, page: int, size: int) -> list[User]:
    """
    Asynchronously fetches a list of users from the database based on the page and size parameters.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        page (int): The page number to fetch.
        size (int): The number of users to fetch per page.

    Returns:
        list[User]: A list of User objects for the specified page and size.
    """
    users = await db.scalars(select(User).limit(size).offset((page - 1) * size))
    return list(users.all())


async def create_user(*, db: AsyncSession, user_in: UserCreate) -> User:
    """
    Asynchronously creates a new user in the database.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        user_in (UserCreate): A UserCreate object containing the new user's information.

    Returns:
        User: The newly created User object.

    Raises:
        HTTPException: If a user with the same username or email already exists,
        a 400 Bad Request exception is raised.
    """
    await check_user_exists(db=db, username=user_in.username, email=user_in.email)
    user = User(username=user_in.username, email=user_in.email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(*, db: AsyncSession, user_in: UserUpdate, user_id: int) -> User:
    """
    Asynchronously updates a user in the database.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        user_in (UserUpdate): A UserUpdate object containing the updated user's information.
        user_id (int): The id of the user to update.

    Returns:
        User: The updated User object.

    Raises:
        HTTPException: If a user with the same username or email already exists,
        a 400 Bad Request exception is raised.
    """
    user = await get_user_by_id(db=db, user_id=user_id)
    await check_user_exists(db=db, username=user_in.username, email=user_in.email)
    await db.execute(update(User).where(User.id == user_id).values(user_in.model_dump()))
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(*, db: AsyncSession, user_id: int) -> None:
    """
    Asynchronously deletes a user from the database.

    Args:
        db (AsyncSession): An asynchronous session for the database.
        user_id (int): The id of the user to delete.
    """
    user = await get_user_by_id(db=db, user_id=user_id)
    await db.delete(user)
    await db.commit()
