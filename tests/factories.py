import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Equipment, Exercise, ExerciseMuscleGroup, MuscleGroup, User, WorkoutSession, Set


@pytest.fixture()
def workout_factory(db_session, test_user):
    
    def create_workout(**kwargs):

        defaults = {
            "user_id": test_user.id,
            "name": "Test Workout",
            "notes": "Test notes"
        }

        defaults.update(**kwargs)

        workout = WorkoutSession(**defaults)

        db_session.add(workout)
        db_session.commit()
        db_session.refresh(workout)

        return workout
    
    return create_workout

@pytest.fixture()
def set_factory(db_session, workout_factory, exercise_factory):

    def create_set(**kwargs):

        workout = workout_factory()
        exercise = exercise_factory()

        defaults = {
            "workout_id": workout.id,
            "exercise_id": exercise.id,
            "set_number": 1,
            "reps": 8,
            "weight": 135,
            "rest": 120
        }

        defaults.update(**kwargs)

        new_set = Set(**defaults)

        db_session.add(new_set)
        db_session.commit()
        db_session.refresh(new_set)

        return new_set
    
    return create_set


@pytest.fixture()
def equipment_factory(db_session):
    
    def create_equipment(**kwargs):

        defaults = {
            "name": "Barbell",
            "input_mode": "barbell"
        }

        defaults.update(**kwargs)

        equipment = Equipment(**defaults)

        db_session.add(equipment)
        db_session.commit()
        db_session.refresh(equipment)


        return equipment
    
    return create_equipment


@pytest.fixture()
def muscle_factory(db_session: Session):

    def create_muscle(**kwargs):

        defaults = {
            "name": "Chest",
            "is_primary": True
        }

        defaults.update(**kwargs)

        muscle = MuscleGroup(**defaults)

        db_session.add(muscle)
        db_session.commit()
        db_session.refresh(muscle)

        return muscle
    
    return create_muscle


@pytest.fixture()
def exercise_factory(db_session: Session, equipment_factory, muscle_factory):
    """
    Args:
        muscles: List of tuples containing muscle_id and role
    Kwargs:
        equipment_id: Id of pre-created equipment
        created_by_user_id: Id of user creator
        name: Name of exercise
    Returns:
        Newly created Exercise
    """
    
    def create_exercise(muscles: list[tuple] | None = None, **kwargs):

        # Check for supplied or existing equipment before calling equipment_factory
        equipment_id = kwargs.get("equipment_id")

        if equipment_id is None:
            equipment = db_session.scalar(select(Equipment))

            if not equipment:
                equipment_id = equipment_factory().id
            else:
                equipment_id = equipment.id
            
        # Check for supplied or existing muscle group before calling muscle_factory
        if not muscles:
            muscle = db_session.scalar(select(MuscleGroup))

            if not muscle:
                muscles = [(muscle_factory().id, "primary")]
            else:
                muscles = [(muscle.id, "primary")]
            

        defaults = {
            "equipment_id": equipment_id,
            "name": "Bench Press"
        }

        defaults.update(**kwargs)

        exercise = Exercise(**defaults)

        for muscle in muscles:
            exercise.muscles.append(
                ExerciseMuscleGroup(
                    muscle_group_id=muscle[0],
                    role=muscle[1]
                )
            )

        db_session.add(exercise)
        db_session.commit()
        db_session.refresh(exercise)
        
        return exercise
    
    return create_exercise

