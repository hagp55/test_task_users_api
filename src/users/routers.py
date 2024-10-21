from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db
from src.users import crud
from src.users.models import User
from src.users.schemas import UserCreate, UserFromDB, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserFromDB], status_code=status.HTTP_200_OK)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0, description="the number of users to skip")] = 0,
    limit: Annotated[int, Query(ge=0, description="the number of users to show")] = 100,
) -> list[User]:
    users = await crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}/", response_model=UserFromDB, status_code=status.HTTP_200_OK)
async def get_user_detail(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
) -> User:
    users = await crud.get_user_by_id(db=db, user_id=user_id)
    return users


@router.post("/", response_model=UserFromDB, status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], user_in: UserCreate) -> User:
    user = await crud.create_user(db=db, user_in=user_in)
    return user


@router.put("/{user_id}/", response_model=UserFromDB, status_code=status.HTTP_200_OK)
async def update_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: Annotated[int, Path(ge=1)],
    user_in: UserUpdate,
) -> User:
    user = await crud.update_user(db=db, user_id=user_id, user_in=user_in)
    return user


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)], user_id: Annotated[int, Path(ge=1)]
) -> None:
    await crud.delete_user(db=db, user_id=user_id)
    return
