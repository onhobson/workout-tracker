from pydantic import BaseModel, ConfigDict

class EquipmentRead(BaseModel):
    id: int
    name: str
    input_mode: str

    model_config = ConfigDict(from_attributes=True)