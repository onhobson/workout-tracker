from fastapi import APIRouter, HTTPException, status

from app.crud import workout as crud_workout
from app.dependencies import *
from app.schemas.workout import WorkoutCreate, WorkoutRead, WorkoutUpdate

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", response_model=list[WorkoutRead])
def get_user_workouts(
    user: CurrentUser, 
    db: DbSession
):
    return crud_workout.get_user_workouts(user.id, db)


@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout(
    workout_id: int, 
    user: CurrentUser, 
    db: DbSession
):
    workout = crud_workout.get_workout(workout_id, user.id, db)

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Workout with id: {workout_id} not found"
        )

    return workout


@router.post("/", response_model=WorkoutRead, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout: WorkoutCreate,
    user: CurrentUser, 
    db: DbSession
):
    return crud_workout.create_workout(workout, user.id, db)


@router.put("/{workout_id}", response_model=WorkoutRead)
def update_workout(
    workout_id: int, 
    workout_update: WorkoutUpdate, 
    user: CurrentUser, 
    db: DbSession
):
    workout = crud_workout.update_workout(workout_id, workout_update, user.id, db)

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Workout with id: {workout_id} not found"
        )
    
    return workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: int, 
    user: CurrentUser, 
    db: DbSession
):
    workout = crud_workout.delete_workout(workout_id, user.id, db)

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Workout with id: {workout_id} not found"
        )

