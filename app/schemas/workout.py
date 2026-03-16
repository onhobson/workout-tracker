"""
Workout schemas for the workout tracker application.
"""
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.core.limits import WORKOUT_NAME_MAX_LENGTH, NOTES_MAX_LENGTH
from app.schemas.set import SetRead

class WorkoutBase(BaseModel):
    name: Annotated[str | None, Field(
        default=None, 
        max_length=WORKOUT_NAME_MAX_LENGTH,
    )]
    notes: Annotated[str | None, Field(
        default=None, 
        max_length=NOTES_MAX_LENGTH,
    )]


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime
    user_id: int

    sets: list[SetRead] = []

    model_config = ConfigDict(from_attributes=True)


class WorkoutUpdate(WorkoutBase):
    pass
    