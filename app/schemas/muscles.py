from pydantic import BaseModel, ConfigDict

class MuscleGroupRead(BaseModel):
    id: int
    muscle: str

    model_config = ConfigDict(from_attributes=True)


class MuscleGroupWithExercises(MuscleGroupRead):
    exercises: list[ExerciseSummary] = []