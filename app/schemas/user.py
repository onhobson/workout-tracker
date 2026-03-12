from pydantic import BaseModel, EmailStr, field_validator

from app.schemas.workout import WorkoutRead


class UserBase(BaseModel):
    username: str
    email: EmailStr

    @field_validator("username", "email")
    def normalize(cls, value: str) -> str:
        return value.lower()


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    workouts: list[WorkoutRead]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("username", "email")
    def normalize(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.lower()