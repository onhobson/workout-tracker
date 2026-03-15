from sqlalchemy import select, insert

from app.db.database import Session
from app.db.models import Equipment, MuscleGroup, Exercise, ExerciseMuscleGroup


EQUIPMENT = [
    {"name": "Barbell", "input_mode": "barbell"},
    {"name": "Dumbbell", "input_mode": "double"},
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
    {"name": "Bench Press", "equipment_id": 1, "created_by_user_id": None},  # Barbell
    {"name": "Incline Bench Press", "equipment_id": 1, "created_by_user_id": None},
    {"name": "Dumbbell Fly", "equipment_id": 2, "created_by_user_id": None},
    {"name": "Push-Up", "equipment_id": 6, "created_by_user_id": None},  # Bodyweight

    # Back
    {"name": "Pull-Up", "equipment_id": 6, "created_by_user_id": None},
    {"name": "Lat Pulldown", "equipment_id": 5, "created_by_user_id": None},  # Cable
    {"name": "Barbell Row", "equipment_id": 1, "created_by_user_id": None},
    {"name": "Dumbbell Row", "equipment_id": 2, "created_by_user_id": None},

    # Shoulders
    {"name": "Overhead Press", "equipment_id": 1, "created_by_user_id": None},
    {"name": "Dumbbell Lateral Raise", "equipment_id": 2, "created_by_user_id": None},
    {"name": "Cable Face Pull", "equipment_id": 5, "created_by_user_id": None},

    # Biceps
    {"name": "Barbell Curl", "equipment_id": 1, "created_by_user_id": None},
    {"name": "Dumbbell Curl", "equipment_id": 2, "created_by_user_id": None},
    {"name": "Hammer Curl", "equipment_id": 2, "created_by_user_id": None},

    # Triceps
    {"name": "Tricep Pushdown", "equipment_id": 5, "created_by_user_id": None},
    {"name": "Dips", "equipment_id": 6, "created_by_user_id": None},
    {"name": "Overhead Dumbbell Extension", "equipment_id": 2, "created_by_user_id": None},

    # Forearms
    {"name": "Wrist Curl", "equipment_id": 2, "created_by_user_id": None},
    {"name": "Reverse Wrist Curl", "equipment_id": 2, "created_by_user_id": None},

    # Legs
    {"name": "Squat", "equipment_id": 1, "created_by_user_id": None},  # Barbell
    {"name": "Leg Press", "equipment_id": 4, "created_by_user_id": None},  # Machine
    {"name": "Lunge", "equipment_id": 2, "created_by_user_id": None},  # Dumbbell
    {"name": "Leg Curl", "equipment_id": 4, "created_by_user_id": None},
    {"name": "Leg Extension", "equipment_id": 4, "created_by_user_id": None},
    {"name": "Calf Raise", "equipment_id": 2, "created_by_user_id": None},

    # Glutes / Hips
    {"name": "Hip Thrust", "equipment_id": 1, "created_by_user_id": None},
    {"name": "Glute Kickback", "equipment_id": 5, "created_by_user_id": None},  # Cable
    {"name": "Abductor Machine", "equipment_id": 4, "created_by_user_id": None},

    # Core / Abs
    {"name": "Crunch", "equipment_id": 6, "created_by_user_id": None},
    {"name": "Plank", "equipment_id": 6, "created_by_user_id": None},
    {"name": "Hanging Leg Raise", "equipment_id": 6, "created_by_user_id": None},
    {"name": "Cable Woodchopper", "equipment_id": 5, "created_by_user_id": None},
]


def seed_equipment():
    with Session() as db:
        existing = db.scalars(select(Equipment.name)).all()
        existing_set = set(existing)

        new_rows = [row for row in EQUIPMENT if row["name"] not in existing_set]

        if new_rows:
            db.execute(insert(Equipment), new_rows)
            db.commit()


def seed_muscle_groups():
    with Session() as db:
        existing = db.scalars(select(MuscleGroup.name)).all()
        existing_set = set(existing)

        new_rows = [row for row in MUSCLE_GROUPS if row["name"] not in existing_set]

        if new_rows:
            db.execute(insert(MuscleGroup), new_rows)
            db.commit()


def seed_exercises():
    with Session() as db:
        existing = db.scalars(select(Exercise.name)).all()
        existing_set = set(existing)

        new_rows = [row for row in EXERCISES if row["name"] not in existing_set]

        if new_rows:
            db.execute(insert(Exercise), new_rows)
            db.commit()



if __name__ == "__main__":
    seed_equipment()
    seed_muscle_groups()
    seed_exercises()