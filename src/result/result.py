from json import JSONEncoder
from typing import List, Optional
from enum import Enum

from src.response.error import Error
from src.response.warning import Warning
from src.response.response import Response


class Result:
    """
    Represents the final result of the analysis.
    Encapsulates all the errors, warnings, and evidence sources returned
    by the performed analysis.
    """
    def __init__(self):
        """
        Constructor for Result class.

        errors (List[Error]): List of errors returned by the Semantic Rules analysis
        warnings (List[Warning]): List of warnings returned by the Semantic Hints analysis
        evidence_sources (Optional[Response]): Evidence sources returned by the Evidence Quality analysis

        """
        self.errors: List[Error] = []
        self.warnings: List[Warning] = []
        self.evidence_sources: Optional[Response] = None


class ResultEncoder(JSONEncoder):
    """
    Custom JSON encoder for Result class.
    """
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return obj.__dict__