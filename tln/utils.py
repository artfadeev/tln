import uuid


class TLNException(Exception):
    """Base exception class"""

    pass


class ReferenceException(TLNException):
    """Raised when reference lookup fails for some reason"""

    pass


def generate_id():
    return str(uuid.uuid4())[-12:]
