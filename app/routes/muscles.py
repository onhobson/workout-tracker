from fastapi import APIRouter, HTTPException, status

from app.crud import muscles as crud_muscles
from app.dependencies import *
from app.schemas.muscles import MuscleGroupRead

router = APIRouter(prefix="/muscles", tags=["Muscles"])


@router.get("/", response_model=list[MuscleGroupRead])
def get_all_muscle_groups(db: DbSession):
    return crud_muscles.get_all_muscle_groups(db)


@router.get("/{muscle_id}", response_model=MuscleGroupRead)
def get_muscle_group(muscle_id: int, db: DbSession):
    muscle_group = crud_muscles.get_muscle_group(muscle_id, db)

    if not muscle_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Muscle group with id: {muscle_id} not found"
        )
    
    return muscle_group