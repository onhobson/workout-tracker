from pydantic import BaseModel, ConfigDict

from app.schemas.common import ExerciseSummary

class MuscleGroupRead(BaseModel):
    id: int
    name: str
    is_primary: bool

    model_config = ConfigDict(from_attributes=True)


class MuscleGroupWithExercises(MuscleGroupRead):
    exercises: list[ExerciseSummary] = []