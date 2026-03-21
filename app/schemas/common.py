"""
Common summary schemas for the workout tracker application.
"""
from pydantic import BaseModel, ConfigDict

from app.db.enums import MuscleRole

class ExerciseSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class MuscleGroupSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class EquipmentSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
    

class ExerciseMuscleSummary(BaseModel):
    muscle: MuscleGroupSummary
    role: MuscleRole

    model_config = ConfigDict(from_attributes=True)