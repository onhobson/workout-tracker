from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import EmptyStringError, InvalidForeignKeyIDError
from app.crud import exercise as crud_exercise
from app.dependencies import *
from app.schemas.common import ExerciseSummary
from app.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", response_model=list[ExerciseSummary])
def get_exercises(
    user: CurrentUser, 
    db: DbSession,
    muscle_id: int | None = None,
    equipment_id: int | None = None
):
    return crud_exercise.get_exercises(muscle_id, equipment_id, user.id, db)


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, user: CurrentUser, db: DbSession):
    exercise = crud_exercise.get_exercise(exercise_id, user.id, db)

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id: {exercise_id} not found"
        )
    
    return exercise


@router.post("/", response_model=ExerciseRead, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise_data: ExerciseCreate, user: CurrentUser, db: DbSession):
    try:
        return crud_exercise.create_exercise(exercise_data, user.id, db)
    except EmptyStringError as e:
        raise HTTPException(
            status_code=422,
            detail=f"{e.field.capitalize()} can not be empty"
        )
    except InvalidForeignKeyIDError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Given {e.field} not found"
        )
    

@router.put("/{exercise_id}", response_model=ExerciseRead)
def update_exercise(exercise_id: int, exercise_data: ExerciseUpdate, user: CurrentUser, db: DbSession):
    try:
        exercise = crud_exercise.update_exercise(exercise_id, exercise_data, user.id, db)
    except EmptyStringError as e:
        raise HTTPException(
            status_code=422,
            detail=f"{e.field.capitalize()} can not be empty"
        )
    except InvalidForeignKeyIDError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Given {e.field} not found"
        )

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id: {exercise_id} not found"
        )

    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int , user: CurrentUser, db: DbSession):
    success = crud_exercise.delete_exercise(exercise_id, user.id, db)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id: {exercise_id} not found"
        )