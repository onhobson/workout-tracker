"""
CRUD operations for workout sessions.
"""
from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import WorkoutSession
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from app.utils.naming import generate_workout_name, parse_suffix

def get_workout(workout_id: int, user_id: int, db: Session) -> WorkoutSession | None:
    """
    Retrieve a specific workout session by ID, ensuring it belongs to the user.
    Returns None if the workout does not exist or does not belong to the user.
    """
    stmt = select(WorkoutSession).where(
        WorkoutSession.id == workout_id, 
        WorkoutSession.user_id == user_id
    )
    return db.scalar(stmt)


def get_user_workouts(user_id: int, db: Session) -> Sequence[WorkoutSession]:
    """
    Retrieve all workout sessions belonging to a specific user.
    Returns a sequence of WorkoutSession objects.
    """
    stmt = select(WorkoutSession).where(WorkoutSession.user_id == user_id)
    return db.scalars(stmt).all()


def create_workout(workout: WorkoutCreate, user_id: int, db: Session) -> WorkoutSession:
    """
    Create a new workout session for a user. If the workout name is not provided, generate a default name based on the current date and existing workouts.

    Args:
        workout: WorkoutCreate data for the new workout session.
        user_id: ID of the user creating the workout session.
        db: Database session for querying and committing the new workout session.
    Returns:
        The created WorkoutSession object.
    """
    if not workout.name:
        today = datetime.now()
        prefix = generate_workout_name(today)

        stmt = (
            select(func.max(WorkoutSession.name))
            .where(
                WorkoutSession.user_id == user_id,
                WorkoutSession.name.startswith(prefix)
            )
        )

        max_name = db.scalar(stmt)
        
        if max_name:
            next_suffix = parse_suffix(max_name) + 1
        else:
            next_suffix = 1
        
        workout.name = generate_workout_name(today, suffix=next_suffix)

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
    """
    Update an existing workout session, ensuring it belongs to the user.

    Args:
        workout_id: ID of the workout session to update.
        workout_update: WorkoutUpdate data containing the fields to update.
        user_id: ID of the user updating the workout session, used to verify ownership.
        db: Database session for querying and committing the updated workout session.
    Returns:
        The updated WorkoutSession object if successful.
        None if the workout does not exist or does not belong to the user.
    """
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
    """
    Delete a specific workout session by ID, ensuring it belongs to the user.
    Returns True if the workout was deleted, False if the workout does not exist or does not belong to the user.
    """
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