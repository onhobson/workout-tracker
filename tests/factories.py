import pytest

from app.db.models import User, WorkoutSession, Set


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
def set_factory(db_session, workout_factory):

    def create_set(**kwargs):

        workout = workout_factory()

        defaults = {
            "workout_id": workout.id,
            "exercise_id": 1,
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