from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import WorkoutSession
from app.schemas.workout import WorkoutCreate, WorkoutUpdate

def get_workout(workout_id: int, user_id: int, db: Session) -> WorkoutSession | None:
    """
    Return one workout by id belonging to a specific user.
    """
    stmt = select(WorkoutSession).where(
        WorkoutSession.id == workout_id, 
        WorkoutSession.user_id == user_id
    )
    return db.scalar(stmt)


def get_user_workouts(user_id: int, db: Session) -> Sequence[WorkoutSession]:
    """
    Return all workouts belonging to a specific user.
    """
    stmt = select(WorkoutSession).where(WorkoutSession.user_id == user_id)
    return db.scalars(stmt).all()


def create_workout(workout: WorkoutCreate, user_id: int, db: Session) -> WorkoutSession:
    new_workout = WorkoutSession(
        user_id = user_id,
        **workout.model_dump(),
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout


def update_workout(
    workout_id: int, 
    workout_update: WorkoutUpdate, 
    user_id: int, 
    db: Session
) -> WorkoutSession | None:
    stmt = select(WorkoutSession).where(
        WorkoutSession.id == workout_id, 
        WorkoutSession.user_id == user_id
    )
    
    workout = db.scalar(stmt)

    if not workout:
        return None

    update_data = workout_update.model_dump(exclude_unset=True)

    for column, value in update_data.items():
        setattr(workout, column, value)

    db.commit()
    db.refresh(workout)
    
    return workout
    

def delete_workout(workout_id: int, user_id: int, db: Session) -> bool:
    stmt = select(WorkoutSession).where(
        WorkoutSession.id == workout_id, 
        WorkoutSession.user_id == user_id
    )

    workout = db.scalar(stmt)

    if not workout:
        return False
    
    db.delete(workout)
    db.commit()

    return True