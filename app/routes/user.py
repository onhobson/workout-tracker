from fastapi import APIRouter, HTTPException, status

from app.crud import user as crud_user
from app.dependencies import *
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserRead)
def get_user(
    user: CurrentUser, 
    db: DbSession
):
    user_found = crud_user.get_user(user.id, db)

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
            )

    return user_found


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: DbSession
):
    return crud_user.create_user(user, db)


@router.put("/", response_model=UserRead)
def update_user(
    user_data: UserUpdate,
    user: CurrentUser,
    db: DbSession
):
    user_update = crud_user.update_user(user_data, user, db)

    if not user_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user.id} not found",
        )
    
    return user_update


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user: CurrentUser,
    db: DbSession
):
    success = crud_user.delete_user(user.id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user.id} not found",
        )