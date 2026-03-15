from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ExerciseSummary

class SetBase(BaseModel):
    workout_id: Annotated[int, Field(ge=0)]
    exercise_id: Annotated[int, Field(ge=0)]
    reps: Annotated[int, Field(ge=0, lt=1000)]
    weight: Annotated[int, Field(default=0, ge=0, lt=10000)]
    rest: Annotated[int | None, Field(default=None, ge=0, lt=10000)]


class SetCreate(SetBase):
    pass


class SetRead(SetBase):
    id: int
    set_number: int

    exercise: ExerciseSummary

    model_config = ConfigDict(from_attributes=True)


class SetUpdate(BaseModel):
    exercise_id: Annotated[int | None, Field(default=None, ge=0)]
    reps: Annotated[int | None, Field(default=None, ge=0, lt=1000)]
    weight:  Annotated[int | None, Field(default=None, ge=0, lt=10000)]
    rest:  Annotated[int | None, Field(default=None, ge=0, lt=10000)]