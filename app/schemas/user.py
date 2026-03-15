from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.workout import WorkoutRead


class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=32)]
    email: Annotated[EmailStr, Field(min_length=1, max_length=254)]

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
    username: Annotated[str | None, Field(default=None, min_length=1, max_length=32)]
    email: Annotated[EmailStr | None, Field(default=None, min_length=1, max_length=254)]
    password: Annotated[str | None, Field(default=None, min_length=1)]

    @field_validator("username", "email")
    def normalize(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.lower()