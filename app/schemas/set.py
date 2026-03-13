from pydantic import BaseModel

from app.schemas.common import ExerciseSummary

class SetBase(BaseModel):
    workout_id: int
    exercise_id: int
    reps: int
    weight: int = 0
    rest: int | None = None


class SetCreate(SetBase):
    pass


class SetRead(SetBase):
    id: int
    set_number: int

    exercise: ExerciseSummary

    class Config:
        from_attributes = True


class SetUpdate(BaseModel):
    exercise_id: int | None = None
    reps: int | None = None
    weight: int | None = None
    rest: int | None = None