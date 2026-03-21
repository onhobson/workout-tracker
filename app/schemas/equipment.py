"""
Equipment schemas for the workout tracker application.
"""
from pydantic import BaseModel, ConfigDict

from app.db.enums import InputMode

class EquipmentRead(BaseModel):
    id: int
    name: str
    input_mode: InputMode

    model_config = ConfigDict(from_attributes=True)