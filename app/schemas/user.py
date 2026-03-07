from pydantic import BaseModel

from schemas.workout import WorkoutRead


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    workouts: list[WorkoutRead]


class UserReadSecret(UserBase):
    id: int
    hashed_password: str


class UserUpdate(BaseModel):
    name: str | None
    email: str | None
    password: str | None