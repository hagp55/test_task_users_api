from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db
from src.users import crud, services
from src.users.models import User
from src.users.schemas import UserCreate, UserFromDB, UserStatistics, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/statistics/", response_model=UserStatistics, status_code=status.HTTP_200_OK)
async def get_user_statistics(
    db: Annotated[AsyncSession, Depends(get_db)],
    domain: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=50,
            regex=r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ] = "example.com",
) -> UserStatistics:
    user_statistics = UserStatistics(
        users_registered_seven_days_ago=await services.count_user_registered_last_seven_days(db=db),
        top_five_users_with_longest_names=await services.top_five_users_with_longest_names(db=db),
        ratio_of_users_with_specific_domain=await services.ratio_of_users_with_specific_domain(
            db=db, domain=domain
        ),
    )
    return user_statistics


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
