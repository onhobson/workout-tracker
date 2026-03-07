from app.db.database import Session
from app.db.models import User, WorkoutSession, Set


def seed():
    db = Session()

    user = User(name="Sample User", email="email@example.com", hashed_password="12345")

    db.add(user)
    db.commit()
    db.refresh(user)

    workout = WorkoutSession(
        user_id=user.id,
        notes="Sample workout",
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    sets = [
        Set(session_id=workout.id, exercise="Bench Press", set_number=1, reps=8, weight=120),
        Set(session_id=workout.id, exercise="Bench Press", set_number=2, reps=6, weight=135),
        Set(session_id=workout.id, exercise="Shoulder Press", set_number=3, reps=8, weight=100),
    ]

    db.add_all(sets)

    db.commit()

    db.close()


if __name__ == "__main__":
    seed()