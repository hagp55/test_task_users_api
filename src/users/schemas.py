from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints


class UserBase(BaseModel):
    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=2),
    ]
    email: EmailStr


class UserFromDB(UserBase):
    id: int
    registration: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserStatistics(BaseModel):
    users_registered_seven_days_ago: int = Field(
        serialization_alias="count_users_registered_seven_days_ago"
    )
    top_five_users_with_longest_names: list[str]
    ratio_of_users_with_specific_domain: float
