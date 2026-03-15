from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.core.limits import EXERCISE_NAME_MAX_LENGTH
from app.schemas.common import MuscleGroupSummary, EquipmentSummary

class ExerciseBase(BaseModel):
    name: Annotated[str, Field(
        min_length=1,
        max_length=EXERCISE_NAME_MAX_LENGTH,
    )]


class ExerciseCreate(ExerciseBase):
    equipment_id: Annotated[int, Field(ge=0)]
    muscle_group_ids: list[Annotated[int, Field(ge=0)]]


class ExerciseRead(ExerciseBase):
    id: int
    
    equipment: EquipmentSummary
    muscles: list[MuscleGroupSummary]

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
    muscle_group_ids: Annotated[list[int] | None, Field(
        default=None,
        ge=0,
    )]