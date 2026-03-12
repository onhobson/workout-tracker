from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.schemas.set import SetRead
from app.utils.naming import generate_workout_name

class WorkoutBase(BaseModel):
    name: str | None = None
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime
    user_id: int

    sets: list[SetRead] = []

    class Config:
        from_attributes = True


class WorkoutUpdate(WorkoutBase):
    pass
    