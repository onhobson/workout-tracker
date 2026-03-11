from pydantic import BaseModel, EmailStr

from app.schemas.workout import WorkoutRead


class UserBase(BaseModel):
    name: str
    email: EmailStr


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
    email: EmailStr | None
    password: str | None