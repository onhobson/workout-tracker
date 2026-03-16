"""
Exercise schemas for the workout tracker application.
"""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.core.limits import EXERCISE_NAME_MAX_LENGTH
from app.schemas.common import ExerciseMuscleSummary, EquipmentSummary

class ExerciseBase(BaseModel):
    name: Annotated[str, Field(
        min_length=1,
        max_length=EXERCISE_NAME_MAX_LENGTH,
    )]

    model_config = ConfigDict(str_strip_whitespace=True)


class ExerciseMuscleCreate(BaseModel):
    muscle_group_id: Annotated[int , Field(ge=0)]
    role: str


class ExerciseCreate(ExerciseBase):
    equipment_id: Annotated[int, Field(ge=0)]
    muscle_groups: list[ExerciseMuscleCreate]


class ExerciseRead(ExerciseBase):
    id: int
    
    equipment: EquipmentSummary
    muscles: list[ExerciseMuscleSummary]

    model_config = ConfigDict(from_attributes=True)


class ExerciseUpdate(BaseModel):
    name: Annotated[str | None, Field(
        default=None,
        min_length=1,
        max_length=EXERCISE_NAME_MAX_LENGTH,
    )]
    equipment_id: Annotated[int | None, Field(
        default=None,
        ge=0,
    )]
    muscle_groups: list[ExerciseMuscleCreate] | None = None
    
    model_config = ConfigDict(str_strip_whitespace=True)