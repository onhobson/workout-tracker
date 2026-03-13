class DuplicateUserError(Exception):
    """Raised when attempting to create a user with a duplicate username or email."""

    def __init__(self, field: str):
        self.field = field
        message = f"{field} already exists"
        super().__init__(message)