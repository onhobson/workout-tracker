"""
User route enpoints.

Provides API routes for reading, updating, 
and deleting an authenticated user, or for creating a new user.
"""
from fastapi import APIRouter, HTTPException, status

from app.crud import user as crud_user
from app.dependencies import *
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.exceptions import DuplicateUserError, EmptyStringError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UserRead)
def get_user(
    user: CurrentUser, 
    db: DbSession
):
    """
    Return user data for currently authenticated user.
    """
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
    """
    Create a new user.
    """
    try: 
        return crud_user.create_user(user, db)
    except DuplicateUserError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Given {e.field} is taken",
        )
    except EmptyStringError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"{e.field.capitalize()} can not be empty"
        )


@router.put("/", response_model=UserRead)
def update_user(
    user_data: UserUpdate,
    user: CurrentUser,
    db: DbSession
):
    """
    Update fields of an authenticated user.
    """
    try:
        user_update = crud_user.update_user(user_data, user, db)
    except EmptyStringError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"{e.field.capitalize()} can not be empty"
        )

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
    """
    Delete the currently authenticated user.
    """
    success = crud_user.delete_user(user.id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user.id} not found",
        )