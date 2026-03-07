from pydantic import BaseModel

class SetBase(BaseModel):
    exercise: str
    set_number: int
    reps: int
    weight: int = 0
    rest: str | None


class SetCreate(SetBase):
    pass


class SetRead(SetBase):
    id: int
    workout_id: int

    class Config:
        from_attributes = True


class SetUpdate(BaseModel):
    id: int
    exercise: str | None
    set_number: int | None
    reps: int | None
    weight: int | None
    rest: int | None