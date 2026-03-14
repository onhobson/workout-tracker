import pytest

from app.db.models import Equipment, Exercise, User, WorkoutSession, Set


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
def exercise_factory(db_session, equipment_factory):
    
    def create_exercise(**kwargs):
        equipment = equipment_factory()

        defaults = {
            "equipment_id": 1,
            "name": "Bench Press"
        }

        defaults.update(**kwargs)

        exercise = Exercise(**defaults)

        db_session.add(exercise)
        db_session.commit()
        db_session.refresh(exercise)
        
        return exercise
    
    return create_exercise