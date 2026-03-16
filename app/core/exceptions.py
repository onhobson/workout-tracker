class DuplicateUserError(Exception):
    """Raised when attempting to create a user with a duplicate username or email."""

    def __init__(self, field: str):
        self.field = field
        message = f"{field} already exists"
        super().__init__(message)


class EmptyStringError(Exception):
    """Raised when a supplied required field contains an empty string."""

    def __init__(self, field: str):
        self.field = field
        message = f"{field} can not be empty"
        super().__init__(message)


class InvalidForeignKeyIDError(Exception):
    """Raised when a foreign key id given in a request body does not correspond to an existing id in the database."""

    def __init__(self, field: str):
        self.field = field
        message = f"No existing {field} found"
        super().__init__(message)