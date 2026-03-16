"""
User schemas for the workout tracker application.
"""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.limits import USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from app.schemas.workout import WorkoutRead


class UserBase(BaseModel):
    username: Annotated[str, Field(
        min_length=1, 
        max_length=USERNAME_MAX_LENGTH,
    )]
    email: Annotated[EmailStr, Field(
        min_length=1, 
        max_length=EMAIL_MAX_LENGTH,
    )]

    @field_validator("username", "email")
    def normalize(cls, value: str) -> str:
        return value.lower()


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=1)]


class UserRead(UserBase):
    id: int

    workouts: list[WorkoutRead]

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Annotated[str | None, Field(
        default=None, 
        min_length=1, 
        max_length=USERNAME_MAX_LENGTH,
    )]
    email: Annotated[EmailStr | None, Field(
        default=None, 
        min_length=1, 
        max_length=EMAIL_MAX_LENGTH,
    )]
    password: Annotated[str | None, Field(
        default=None, 
        min_length=1,
    )]

    @field_validator("username", "email")
    def normalize(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.lower()