from sqlalchemy import CheckConstraint


def range_constraint(column: str, min_val: int, max_val: int | None = None, name: str | None = None):
    """
    Takes a column name to be constrained, min_val (inclusive), an optional max_val, and an optional constraint name.
    """
    sql_string = f"{column} >= {min_val}"

    if max_val is not None:
        sql_string += f" AND {column} <= {max_val}"

    return CheckConstraint(sqltext=sql_string, name=name)