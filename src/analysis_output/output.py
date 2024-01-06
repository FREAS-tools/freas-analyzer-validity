from json import JSONEncoder
from typing import List, Optional
from enum import Enum

from src.rules.rule_result.result import Result


class Output:
    """
    Represents the final output of the analysis.
    Encapsulates all the errors, warnings, and evidence sources returned
    by the performed analysis.
    """
    def __init__(self):
        """
        Constructor for Output class.

        errors (List[Result]): List of errors returned by the Semantic Rules analysis
        warnings (List[Result]): List of warnings returned by the Semantic Hints analysis
        evidence_sources (Optional[Result]): Evidence sources returned by the Evidence Quality analysis

        """
        self.errors: List[Result] = []
        self.warnings: List[Result] = []
        self.evidence_sources: Optional[Result] = None


class OutputEncoder(JSONEncoder):
    """
    Custom JSON encoder for Output class.
    """
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return obj.__dict__