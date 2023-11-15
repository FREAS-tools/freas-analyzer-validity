from enum import Enum

class Severity(Enum):
    """
    Represents the levels of severity of the error.
    """
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3,
    CRITICAL = 4