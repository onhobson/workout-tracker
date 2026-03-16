"""
Normalization utilities for the workout tracker application.
"""
from typing import Any

USER_INFO_TO_NORMALIZE = ["username", "email"]

def normalize_user_info(user_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize user information by lowercasing and stripping whitespace from pre-specified fields.
    
    Args:
        user_dict: A dictionary containing user information.
    Returns:
        A dictionary with the pre-specified fields normalized.
    """
    for field in USER_INFO_TO_NORMALIZE:
        if field in user_dict and user_dict[field] is not None:
            user_dict[field] = user_dict[field].lower().strip()
    return user_dict