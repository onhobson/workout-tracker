"""
API routes for equipment in the workout tracker application.
"""
from fastapi import APIRouter, HTTPException, status

from app.crud import equipment as crud_equipment
from app.dependencies import *
from app.schemas.equipment import EquipmentRead

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.get("/", response_model=list[EquipmentRead])
def get_all_equipment(db: DbSession):
    """Fetches all equipment available in the workout tracker application."""
    return crud_equipment.get_all_equipment(db)


@router.get("/{equipment_id}", response_model=EquipmentRead)
def get_equipment(equipment_id: int, db: DbSession):
    """Fetches a specific piece of equipment by ID."""
    equipment = crud_equipment.get_equipment(equipment_id, db)

    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipment with id: {equipment_id} not found"
        )
    
    return equipment