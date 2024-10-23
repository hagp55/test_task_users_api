from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints


class UserBase(BaseModel):
    """
    A base model for a User.

    Attributes:
        username (str): The username of the user.
        email (str): The email of the user.
    """

    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=2),
    ]
    email: EmailStr


class UserFromDB(UserBase):
    """
    A model for a User retrieved from the database.

    Inherits from UserBase.

    Attributes:
        id (int): The unique identifier for the user.
        registration (datetime): The date and time when the user was registered.
    """

    id: int
    registration: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    A model for creating a new User.

    Inherits from UserBase.
    """


class UserUpdate(UserCreate):
    """
    A model for updating a User.

    Inherits from UserCreate.
    """


class UserStatistics(BaseModel):
    """
    A model for user statistics.

    Attributes:
        users_registered_seven_days_ago (int):
            The number of users registered in the last seven days.
        top_five_users_with_longest_names (list[str]):
             A list of the top five users with the longest names.
        ratio_of_users_with_specific_domain (float):
            The ratio of users with a specific domain to the total number of users.
    """

    users_registered_seven_days_ago: int = Field(
        serialization_alias="count_users_registered_seven_days_ago"
    )
    top_five_users_with_longest_names: list[str]
    percent_of_users_with_specific_domain: str
