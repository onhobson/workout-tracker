from fastapi import APIRouter, HTTPException, status

from app.crud import set as crud_set
from app.dependencies import *
from app.schemas.set import SetRead

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.get("/{set_id}", response_model=SetRead)
def get_set(
    set_id: int, 
    db: DbSession
):
    set = crud_set.get_set(set_id, db)
    
    if not set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Set with id: {set_id} not found"
        )

    return set