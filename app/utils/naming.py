"""
Naming utilities for the workout tracker application.
"""
from datetime import datetime
import re

def generate_workout_name(base_date: datetime, suffix: int | None = None) -> str:
    """
    Generate a workout name based on the given date and optional suffix.
    
    Args:
        base_date: The date to base the workout name on.
        suffix: An optional numeric suffix to differentiate workouts on the same day.
    Returns:
        A string in the format "Workout on Mar 12, 2026" or "Workout on Mar 12, 2026 (2)" if suffix is provided.
    """
    workout_name = f"Workout on {base_date.strftime('%b %d, %Y')}"
    if suffix and suffix > 1:
        workout_name += f" ({suffix})"
    return workout_name


def parse_suffix(name: str) -> int:
    """
    Extract numeric suffix from a name like 'Workout on Mar 12, 2026 (2)'.
    Return 1 if no suffix is found.
    """
    match = re.search(r"\((\d+)\)$", name)
    if match:
        return int(match.group(1))
    return 1