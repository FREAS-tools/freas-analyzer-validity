from typing import List, Optional


class Response:
    """
    Represents a general response returned by a rule.
    Return value of 'EVIDENCE_QUALITY_ANALYSIS' analysis.
    """
    def __init__(self, message: str = "", source: Optional[List[str]] = None):
        """
        Constructor for Response class.

        Parameters:
            message (str): Message describing the response
            source (Optional[List[str]]): Elements supporting the response
        """
        self.source: List[str] = source if source is not None else []
        self.message: str = message
