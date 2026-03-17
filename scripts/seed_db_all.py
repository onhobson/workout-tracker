"""
Comprehensive script to reset the database and seed it with reference and initial data for the workout tracker application.
This script combines the functionality of reset_db.py, seed_db.py, and seed_reference_data.py.
"""
from scripts.reset_db import reset_db
from scripts.seed_db import seed
from scripts.seed_reference_data import seed_all

if __name__ == "__main__":
    reset_db()
    seed_all()
    seed()