from sqlalchemy import select, insert

from app.db.database import Session
from app.db.models import Equipment, MuscleGroup, Exercise, ExerciseMuscleGroup


EQUIPMENT = [
    {"name": "Barbell", "input_mode": "barbell"},
    {"name": "Dumbbell", "input_mode": "double"},
    {"name": "Dumbbell, Single", "input_mode": "single"},
    {"name": "Kettlebell", "input_mode": "single"},
    {"name": "Machine", "input_mode": "single"},
    {"name": "Cable", "input_mode": "single"},
    {"name": "Bodyweight", "input_mode": "single"},
    {"name": "Other", "input_mode": "single"},
]

MUSCLE_GROUPS = [
    # Primary muscles
    {"name": "Chest", "is_primary": True},
    {"name": "Back", "is_primary": True},
    {"name": "Shoulders", "is_primary": True},

    {"name": "Biceps", "is_primary": True},
    {"name": "Triceps", "is_primary": True},
    {"name": "Forearms", "is_primary": True},
    
    {"name": "Quads", "is_primary": True},
    {"name": "Hamstrings", "is_primary": True},
    {"name": "Glutes", "is_primary": True},
    {"name": "Calves", "is_primary": True},

    {"name": "Core", "is_primary": True},

    # Secondary muscles
    {"name": "Upper Chest", "is_primary": False},
    {"name": "Lower Chest", "is_primary": False},

    {"name": "Upper Back", "is_primary": False},
    {"name": "Lats", "is_primary": False},
    {"name": "Lower Back", "is_primary": False},
    {"name": "Traps", "is_primary": False},
    {"name": "Rhomboids", "is_primary": False},

    {"name": "Front Delts", "is_primary": False},
    {"name": "Lateral Delts", "is_primary": False},
    {"name": "Rear Delts", "is_primary": False},

    {"name": "Obliques", "is_primary": False},
    {"name": "Hip Flexors", "is_primary": False},
    {"name": "Adductors", "is_primary": False},
    {"name": "Abductors", "is_primary": False},

    {"name": "Full Body", "is_primary": False},
]


EXERCISES = [
    # Chest
    {"name": "Bench Press", "equipment": "Barbell"},  # Barbell
    {"name": "Incline Bench Press", "equipment": "Dumbbell"},
    {"name": "Dumbbell Fly", "equipment": "Dumbbell"},
    {"name": "Push-Up", "equipment": "Bodyweight"},  # Bodyweight

    # Back
    {"name": "Pull-Up", "equipment": "Bodyweight"},
    {"name": "Lat Pulldown", "equipment": "Cable"},  # Cable
    {"name": "Barbell Row", "equipment": "Barbell"},
    {"name": "Dumbbell Row", "equipment": "Dumbbell"},

    # Shoulders
    {"name": "Overhead Press", "equipment": "Barbell"},
    {"name": "Dumbbell Lateral Raise", "equipment": "Dumbbell"},
    {"name": "Cable Face Pull", "equipment": "Cable"},

    # Biceps
    {"name": "Barbell Curl", "equipment": "Barbell"},
    {"name": "Dumbbell Curl", "equipment": "Dumbbell"},
    {"name": "Hammer Curl", "equipment": "Dumbbell"},

    # Triceps
    {"name": "Tricep Pushdown", "equipment": "Cable"},
    {"name": "Dips", "equipment": "Bodyweight"},
    {"name": "Overhead Dumbbell Extension", "equipment": "Dumbbell"},

    # Forearms
    {"name": "Wrist Curl", "equipment": "Dumbbell"},
    {"name": "Reverse Wrist Curl", "equipment": "Dumbbell"},

    # Legs
    {"name": "Squat", "equipment": "Barbell"},  # Barbell
    {"name": "Leg Press", "equipment": "Machine"},  # Machine
    {"name": "Lunge", "equipment": "Dumbbell"},  # Dumbbell
    {"name": "Leg Curl", "equipment": "Machine"},
    {"name": "Leg Extension", "equipment": "Machine"},
    {"name": "Calf Raise", "equipment": "Dumbbell"},

    # Glutes / Hips
    {"name": "Hip Thrust", "equipment": "Barbell"},
    {"name": "Glute Kickback", "equipment": "Cable"},  # Cable
    {"name": "Abductor Machine", "equipment": "Machine"},

    # Core / Abs
    {"name": "Crunch", "equipment": "Bodyweight"},
    {"name": "Plank", "equipment": "Bodyweight"},
    {"name": "Hanging Leg Raise", "equipment": "Bodyweight"},
    {"name": "Cable Woodchopper", "equipment": "Cable"},
]


EXERCISE_MUSCLES = {
    "Bench Press": [("Chest", "primary"), ("Triceps", "secondary"), ("Front Delts", "secondary")],
    "Incline Bench Press": [("Upper Chest", "primary"), ("Triceps", "secondary"), ("Front Delts", "secondary")],
    "Dumbbell Fly": [("Chest", "primary")],
    "Push-Up": [("Chest", "primary"), ("Triceps", "secondary"), ("Front Delts", "secondary")],
    "Pull-Up": [("Lats", "primary"), ("Biceps", "secondary"), ("Upper Back", "secondary")],
    "Lat Pulldown": [("Lats", "primary"), ("Biceps", "secondary")],
    "Barbell Row": [("Upper Back", "primary"), ("Lats", "secondary"), ("Biceps", "secondary")],
    "Dumbbell Row": [("Upper Back", "primary"), ("Lats", "secondary"), ("Biceps", "secondary")],
    "Overhead Press": [("Shoulders", "primary"), ("Triceps", "secondary")],
    "Dumbbell Lateral Raise": [("Lateral Delts", "primary")],
    "Cable Face Pull": [("Rear Delts", "primary"), ("Traps", "secondary")],
    "Barbell Curl": [("Biceps", "primary")],
    "Dumbbell Curl": [("Biceps", "primary")],
    "Hammer Curl": [("Biceps", "primary"), ("Forearms", "secondary")],
    "Tricep Pushdown": [("Triceps", "primary")],
    "Dips": [("Triceps", "primary"), ("Chest", "secondary")],
    "Overhead Dumbbell Extension": [("Triceps", "primary")],
    "Wrist Curl": [("Forearms", "primary")],
    "Reverse Wrist Curl": [("Forearms", "primary")],
    "Squat": [("Quads", "primary"), ("Glutes", "secondary"), ("Hamstrings", "secondary")],
    "Leg Press": [("Quads", "primary"), ("Glutes", "secondary"), ("Hamstrings", "secondary")],
    "Lunge": [("Quads", "primary"), ("Glutes", "secondary"), ("Hamstrings", "secondary")],
    "Leg Curl": [("Hamstrings", "primary")],
    "Leg Extension": [("Quads", "primary")],
    "Calf Raise": [("Calves", "primary")],
    "Hip Thrust": [("Glutes", "primary")],
    "Glute Kickback": [("Glutes", "primary")],
    "Abductor Machine": [("Abductors", "primary")],
    "Crunch": [("Core", "primary")],
    "Plank": [("Core", "primary")],
    "Hanging Leg Raise": [("Core", "primary")],
    "Cable Woodchopper": [("Obliques", "primary")],
}


def seed_equipment():
    with Session() as db:
        existing = set(db.scalars(select(Equipment.name)).all())

        new_rows = [row for row in EQUIPMENT if row["name"] not in existing]

        if new_rows:
            db.execute(insert(Equipment), new_rows)
            db.commit()


def seed_muscle_groups():
    with Session() as db:
        existing = set(db.scalars(select(MuscleGroup.name)).all())

        new_rows = [row for row in MUSCLE_GROUPS if row["name"] not in existing]

        if new_rows:
            db.execute(insert(MuscleGroup), new_rows)
            db.commit()


def seed_exercises():
    with Session() as db:
        equipment_map = {e.name: e.id for e in db.scalars(select(Equipment)).all()}

        ex_rows = []
        for row in EXERCISES:
            ex_rows.append({
                "name": row["name"],
                "equipment_id": equipment_map[row["equipment"]]
            })

        existing = set(db.scalars(select(Exercise.name)).all())

        new_rows = [row for row in ex_rows if row["name"] not in existing]

        if new_rows:
            db.execute(insert(Exercise), new_rows)
            db.commit()


def seed_exercise_muscle_mapping():
    with Session() as db:
        muscle_map = {m.name: m.id for m in db.scalars(select(MuscleGroup)).all()}
        exercise_map = {e.name: e.id for e in db.scalars(select(Exercise)).all()}

        emg_rows = []
        for ex_name, muscles in EXERCISE_MUSCLES.items():
            ex_id = exercise_map.get(ex_name)

            if not ex_id:
                continue

            for mu_name, role in muscles:
                mu_id = muscle_map.get(mu_name)

                if mu_id:
                    emg_rows.append({
                        "exercise_id": ex_id,
                        "muscle_group_id": mu_id,
                        "role": role
                    })

        existing = set(
            (row.exercise_id, row.muscle_group_id)
            for row in db.scalars(select(ExerciseMuscleGroup)).all()
        )

        new_rows = [row for row in emg_rows if (row["exercise_id"], row["muscle_group_id"]) not in existing]

        if new_rows:
            db.execute(insert(ExerciseMuscleGroup), new_rows)
            db.commit()



if __name__ == "__main__":
    seed_equipment()
    seed_muscle_groups()
    seed_exercises()
    seed_exercise_muscle_mapping()