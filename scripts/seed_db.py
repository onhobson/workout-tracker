"""
Database seeding script for the workout tracker application.
This script populates the database with initial data for testing and development purposes.
Note: Run the reset_db.py script before this to ensure a clean database state.
"""
from app.db.database import Session
from app.db.models import User, WorkoutSession, Set


def seed():
    db = Session()

    user = User( # pw = 12345
        username="sampleuser", 
        email="email@example.com", 
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$4UBJ9OsZrPs4HYb8ADuhVA$2zLNSop23Cc1rWY9kbcOnnhDOaSQ1yp7SIbWxUneJ/U",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    workouts = [
        WorkoutSession(
            user_id=user.id,
            name="Sample workout",
            notes="Sample note",
        ),
        WorkoutSession(
            user_id=user.id,
            name="Empty workout",
        ),
    ]

    db.add_all(workouts)
    db.commit()
    db.refresh(workouts[0])
    db.refresh(workouts[1])

    sets = [
        Set(workout_id=workouts[0].id, exercise_id=1, set_number=1, reps=8, weight=120),
        Set(workout_id=workouts[0].id, exercise_id=1, set_number=2, reps=6, weight=135),
        Set(workout_id=workouts[0].id, exercise_id=2, set_number=1, reps=8, weight=100),
    ]

    db.add_all(sets)
    db.commit()
    db.close()


if __name__ == "__main__":
    seed()