from typing import List, Optional

from src.rules.rule_result.severity import Severity


class Result:
    """
    Represents the result returned by a rule.
    Return value of the analyses.
    """
    def __init__(self, message: str = "", source: Optional[List[str]] = None, severity: Optional[Severity] = None):
        """
        Constructor for Result class.

        Parameters:
            message (str): Message describing the result
            source (Optional[List[str]]): Elements supporting the result
            severity (Optional[Severity]): Severity of the result, if defined
        """
        self.source: List[str] = source if source is not None else []
        self.message: str = message
        self.severity: Optional[Severity] = severity
