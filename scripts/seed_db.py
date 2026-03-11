from app.db.database import Session
from app.db.models import User, WorkoutSession, Set


def seed():
    db = Session()

    user = User( # pw = 12345
        username="SampleUser", 
        email="email@example.com", 
        password="$argon2id$v=19$m=65536,t=3,p=4$4UBJ9OsZrPs4HYb8ADuhVA$2zLNSop23Cc1rWY9kbcOnnhDOaSQ1yp7SIbWxUneJ/U",
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

    sets = [
        Set(workout_id=workouts[0].id, exercise="Bench Press", set_number=1, reps=8, weight=120),
        Set(workout_id=workouts[0].id, exercise="Bench Press", set_number=2, reps=6, weight=135),
        Set(workout_id=workouts[0].id, exercise="Shoulder Press", set_number=3, reps=8, weight=100),
    ]

    db.add_all(sets)

    db.commit()

    db.close()


if __name__ == "__main__":
    seed()