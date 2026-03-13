from app.db.database import Session
from app.db.models import Equipment, Exercise, ExerciseMuscleGroup, MuscleGroup, User, WorkoutSession, Set


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

    equipment = Equipment(
        name="Equipment",
        input_mode="Dumbbell",
    )

    db.add(equipment)
    db.commit()

    muscle = MuscleGroup(
        name="Muscle",
    )

    db.add(muscle)
    db.commit()

    exercises = [
        Exercise(equipment_id=1, name="Exercise"),
        Exercise(equipment_id=1, name="Other exercise"),
    ]

    db.add_all(exercises)
    db.commit()

    assoc = ExerciseMuscleGroup(
        exercise_id=1,
        muscle_group_id=1,
        role="primary",
    )

    db.add(assoc)
    db.commit()

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