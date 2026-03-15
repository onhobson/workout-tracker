from sqlalchemy import select, insert

from app.db.database import Session
from app.db.models import Equipment, MuscleGroup


EQUIPMENT = [
    {"name": "Barbell", "input_mode": "barbell"},
    {"name": "Dumbbell", "input_mode": "double"},
    {"name": "Kettlebell", "input_mode": "single"},
    {"name": "Machine", "input_mode": "single"},
    {"name": "Cable", "input_mode": "single"},
    {"name": "Bodyweight", "input_mode": "single"},
    {"name": "Other", "input_mode": "single"},
]

def seed_exercises():
    with Session() as db:
        existing = db.scalars(select(Equipment.name)).all()
        existing_set = set(existing)

        new_rows = [row for row in EQUIPMENT if row["name"] not in existing_set]

        if new_rows:
            db.execute(insert(Equipment), new_rows)
            db.commit()


if __name__ == "__main__":
    seed_exercises()