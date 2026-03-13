from pydantic import BaseModel, ConfigDict

class ExerciseSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MuscleGroupSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)