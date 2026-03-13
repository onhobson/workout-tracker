from typing import Any

USER_INFO_TO_NORMALIZE = ["username", "email"]

def normalize_user_info(user_dict: dict[str, Any]) -> dict[str, Any]:
    for field in USER_INFO_TO_NORMALIZE:
        if field in user_dict and user_dict[field] is not None:
            user_dict[field] = user_dict[field].lower().strip()
    return user_dict