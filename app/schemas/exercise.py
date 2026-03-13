from pydantic import BaseModel, ConfigDict

from app.schemas.common import MuscleGroupSummary
from app.schemas.equipment import EquipmentRead

class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    equipment_id: int
    muscle_group_ids: list[int]


class ExerciseRead(ExerciseBase):
    id: int
    
    equipment: EquipmentRead
    muscles: list[MuscleGroupSummary]

    model_config = ConfigDict(from_attributes=True)


class ExerciseUpdate(BaseModel):
    name: str | None = None
    equipment_id: int | None = None
    muscle_group_ids: list[int] | None = None