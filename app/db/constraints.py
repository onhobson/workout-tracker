"""
Database constraints for SQLAlchemy models.
"""
from sqlalchemy import CheckConstraint


def range_constraint(column: str, min_val: int, max_val: int | None = None, name: str | None = None):
    """
    Create a CheckConstraint for a column to ensure its value is within a specified range.

    Args:
        column: The name of the column to apply the constraint to.
        min_val: The minimum value allowed for the column.
        max_val: The maximum value allowed for the column (optional).
        name: The name of the constraint (optional).
    Returns:
        A CheckConstraint object that can be added to a SQLAlchemy model.
    """
    sql_string = f"{column} >= {min_val}"

    if max_val is not None:
        sql_string += f" AND {column} <= {max_val}"

    return CheckConstraint(sqltext=sql_string, name=name)