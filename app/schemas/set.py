from pydantic import BaseModel

class SetBase(BaseModel):
    workout_id: int
    exercise: str
    set_number: int
    reps: int
    weight: int = 0
    rest: int | None


class SetCreate(SetBase):
    pass


class SetRead(SetBase):
    id: int

    class Config:
        from_attributes = True


class SetUpdate(BaseModel):
    exercise: str | None = None
    set_number: int | None = None
    reps: int | None = None
    weight: int | None = None
    rest: int | None = None