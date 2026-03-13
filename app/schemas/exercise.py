from pydantic import BaseModel, ConfigDict

class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    equipment_id: int
    muscle_group_ids: list[int]


class ExerciseRead(ExerciseBase):
    id: int
    
    equipment: EquipmentRead
    muscles: list[MuscleGroupRead]

    model_config = ConfigDict(from_attributes=True)


class ExerciseUpdate(BaseModel):
    name: str | None = None
    equipment_id: int | None = None
    muscle_group_ids: list[int] | None = None
    