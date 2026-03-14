from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.set import SetRead

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

    model_config = ConfigDict(from_attributes=True)


class WorkoutUpdate(WorkoutBase):
    pass
    