from fastapi import APIRouter, HTTPException, status

from app.crud import equipment as crud_equipment
from app.dependencies import *
from app.schemas.equipment import EquipmentRead

router = APIRouter(prefix="/equipment", tags=["Equipment"])
