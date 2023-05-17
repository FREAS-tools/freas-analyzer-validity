from typing import List, Optional

from response.response import Response


class Warning(Response):
    """
    Represents a rule response in case of Semantic Hints analysis.
    """
    def __init__(self, message: str = "", source: Optional[List[str]] = None):
        """
        Constructor for Warning class.

        Parameters:
            message (str): Message describing the warning
            source (Optional[List[str]]): Element that caused the warning
        """
        super().__init__(message, source)
