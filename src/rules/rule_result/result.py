from typing import List, Optional


class Result:
    """
    Represents a general result returned by a rule.
    Return value of 'EVIDENCE_QUALITY_ANALYSIS' analysis.
    """
    def __init__(self, message: str = "", source: Optional[List[str]] = None):
        """
        Constructor for Result class.

        Parameters:
            message (str): Message describing the result
            source (Optional[List[str]]): Elements supporting the result
        """
        self.source: List[str] = source if source is not None else []
        self.message: str = message
