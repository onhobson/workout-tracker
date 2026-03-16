from typing import Sequence

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.core.exceptions import EmptyStringError, InvalidForeignKeyIDError
from app.db.models import Equipment, Exercise, ExerciseMuscleGroup, MuscleGroup
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_exercises(
    muscle_id: int | None, 
    equipment_id: int | None,
    user_id: int,
    db: Session
) -> Sequence[Exercise]:
    stmt = select(Exercise).where(
        or_(
            Exercise.created_by_user_id.is_(None),
            Exercise.created_by_user_id == user_id
        )
    )

    if equipment_id:
        stmt = stmt.where(
            Exercise.equipment_id == equipment_id
        )
    
    if muscle_id:
        stmt = stmt.join(ExerciseMuscleGroup).where(
            ExerciseMuscleGroup.muscle_group_id == muscle_id
        )

    return db.scalars(stmt).all()


def get_exercise(exercise_id: int, user_id: int, db: Session) -> Exercise | None:
    stmt = (
        select(Exercise)
        .where(
            Exercise.id == exercise_id,
            or_(
                Exercise.created_by_user_id.is_(None),
                Exercise.created_by_user_id == user_id
            )
        )
    )

    return db.scalar(stmt)


def create_exercise(exercise_data: ExerciseCreate, user_id: int, db: Session) -> Exercise:
    if exercise_data.name.strip() == "":
        raise EmptyStringError("name")

    for muscle in exercise_data.muscle_groups:
        if not db.get(MuscleGroup, muscle.muscle_group_id):
            raise InvalidForeignKeyIDError(f"muscle_group_id: {muscle.muscle_group_id}")
    
    if not db.get(Equipment, exercise_data.equipment_id):
        raise InvalidForeignKeyIDError(f"equipment_id: {exercise_data.equipment_id}")
 
    exercise = Exercise(
        name=exercise_data.name,
        equipment_id=exercise_data.equipment_id,
        created_by_user_id=user_id,
    )

    db.add(exercise)
    db.flush()

    for muscle in exercise_data.muscle_groups:
        exercise.muscles.append(
            ExerciseMuscleGroup(
                muscle_group_id=muscle.muscle_group_id,
                role=muscle.role,
            )
        )

    db.commit()
    db.refresh(exercise)

    return exercise


def update_exercise(exercise_id: int, exercise_data: ExerciseUpdate, user_id: int, db: Session) -> Exercise | None:
    if exercise_data.muscle_groups:
        for muscle in exercise_data.muscle_groups:
            if not db.get(MuscleGroup, muscle.muscle_group_id):
                raise InvalidForeignKeyIDError(f"muscle_group_id: {muscle.muscle_group_id}")
    
    if exercise_data.equipment_id and not db.get(Equipment, exercise_data.equipment_id):
        raise InvalidForeignKeyIDError(f"equipment_id: {exercise_data.equipment_id}")
 
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.created_by_user_id == user_id
    )

    exercise = db.scalar(stmt)

    if not exercise:
        return None
    
    if exercise_data.name:
        exercise.name = exercise_data.name

    if exercise_data.equipment_id:
        exercise.equipment_id = exercise_data.equipment_id

    if exercise_data.muscle_groups:
        exercise.muscles.clear()

        for muscle in exercise_data.muscle_groups:
            exercise.muscles.append(
                ExerciseMuscleGroup(
                    muscle_group_id=muscle.muscle_group_id,
                    role=muscle.role
                )
            )

    db.commit()
    db.refresh(exercise)

    return exercise


def delete_exercise(exercise_id: int, user_id: int, db: Session) -> bool:
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.created_by_user_id == user_id
    )

    exercise = db.scalar(stmt)

    if not exercise:
        return False
    
    db.delete(exercise)
    db.commit()

    return True