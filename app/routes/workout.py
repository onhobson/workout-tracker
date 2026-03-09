from fastapi import APIRouter

from app.crud import workout as crud_workout
from app.dependencies import *
from app.schemas.workout import WorkoutRead

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", response_model=list[WorkoutRead])
def get_user_workouts(user: CurrentUser, db: DbSession):
    return crud_workout.get_user_workouts(user.id, db)


@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout(workout_id: int, db: DbSession):
    return crud_workout.get_workout(workout_id, db)


@router.get("/{workout_id}/sets", response_model=WorkoutRead)
def get_workout_with_sets(workout_id: int, db: DbSession):
    return crud_workout.get_workout_with_sets(workout_id, db)