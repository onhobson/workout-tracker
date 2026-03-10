from fastapi import APIRouter, HTTPException, status

from app.crud import workout as crud_workout
from app.dependencies import *
from app.schemas.workout import WorkoutCreate, WorkoutRead

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", response_model=list[WorkoutRead])
def get_user_workouts(user: CurrentUser, db: DbSession):
    return crud_workout.get_user_workouts(user.id, db)


@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout(workout_id: int, db: DbSession):
    workout = crud_workout.get_workout(workout_id, db)

    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workout with id: {workout_id} not found")
        
    return workout


@router.get("/{workout_id}/sets", response_model=WorkoutRead)
def get_workout_with_sets(workout_id: int, db: DbSession):
    return crud_workout.get_workout_with_sets(workout_id, db)