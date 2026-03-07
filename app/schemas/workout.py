from datetime import datetime

from pydantic import BaseModel

from schemas.set import SetRead

class WorkoutBase(BaseModel):
    name: str
    notes: str | None = None


class WorkoutCreate(BaseModel):
    name: str | None = None


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime
    user_id: int

    sets: list[SetRead] = []

    class Config:
        from_attributes = True


class WorkoutUpdate(BaseModel):
    id: int
    name: str | None = None
    notes: str | None = None
    