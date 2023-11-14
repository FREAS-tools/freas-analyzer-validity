from typing import Optional, List

from src.rules.rule_result.result import Result
from src.rules.rule_result.severity import Severity


class Error(Result):
    """
    Represents a rule result in case of 'SEMANTIC_RULES' analysis.
    """
    def __init__(self, message: str = "", source: Optional[List[str]] = None, severity: Optional[Severity] = None):
        """
        Constructor for Error class.

        Parameters:
            message (str): Message describing the error
            source (Optional[List[str]]): Element that caused the error
            severity (Optional[Severity]): Severity of the error
        """
        super().__init__(message, source)

        self.severity: Optional[Severity] = severity
