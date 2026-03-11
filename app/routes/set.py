from fastapi import APIRouter, HTTPException, status

from app.crud import set as crud_set
from app.dependencies import *
from app.schemas.set import SetCreate, SetRead, SetUpdate

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.get("/{set_id}", response_model=SetRead)
def get_set(
    set_id: int, 
    user: CurrentUser,
    db: DbSession
):
    workout_set = crud_set.get_set(set_id, user.id, db)
    
    if not workout_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Set with id: {set_id} not found"
        )

    return workout_set


@router.post("/", response_model=SetRead, status_code=status.HTTP_201_CREATED)
def create_set(
    set_data: SetCreate,
    db: DbSession
):
    return  crud_set.create_set(set_data, db)


@router.put("/{set_id}", response_model=SetRead)
def update_set(
    set_id: int,
    set_data: SetUpdate,
    user: CurrentUser,
    db: DbSession
):
    workout_set = crud_set.update_set(set_id, set_data, user.id, db)

    if not workout_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with id: {set_id} not found"
        )
    
    return workout_set


@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_set(
    set_id: int,
    user: CurrentUser,
    db: DbSession
):
    workout_set = crud_set.delete_set(set_id, user.id, db)

    if not workout_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Set with id: {set_id} not found"
        )

