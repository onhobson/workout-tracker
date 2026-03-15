from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.set import SetRead

class WorkoutBase(BaseModel):
    name: Annotated[str | None, Field(default=None, max_length=100)]
    notes: Annotated[str | None, Field(default=None, max_length=500)]


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
    