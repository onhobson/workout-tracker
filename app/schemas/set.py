"""
Set schemas for the workout tracker application."""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

import app.core.limits as LIMIT
from app.schemas.common import ExerciseSummary

class SetBase(BaseModel):
    workout_id: Annotated[int, Field(ge=0)]
    exercise_id: Annotated[int, Field(ge=0)]
    reps: Annotated[int, Field(
        ge=LIMIT.REPS_MIN, 
        lt=LIMIT.REPS_MAX,
    )]
    weight: Annotated[int, Field(
        default=0, 
        ge=LIMIT.WEIGHT_MIN, 
        lt=LIMIT.WEIGHT_MAX,
    )]
    rest: Annotated[int | None, Field(
        default=None, 
        ge=LIMIT.REST_MIN, 
        lt=LIMIT.REST_MAX,
    )]


class SetCreate(SetBase):
    pass


class SetRead(SetBase):
    id: int
    set_number: int

    exercise: ExerciseSummary

    model_config = ConfigDict(from_attributes=True)


class SetUpdate(BaseModel):
    exercise_id: Annotated[int | None, Field(default=None, ge=0)]
    reps: Annotated[int | None, Field(
        default=None,
        ge=LIMIT.REPS_MIN, 
        lt=LIMIT.REPS_MAX,
    )]
    weight:  Annotated[int | None, Field(
        default=None, 
        ge=LIMIT.WEIGHT_MIN, 
        lt=LIMIT.WEIGHT_MAX,
    )]
    rest:  Annotated[int | None, Field(
        default=None, 
        ge=LIMIT.REST_MIN, 
        lt=LIMIT.REST_MAX,
    )]