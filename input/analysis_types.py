from enum import Enum


class AnalysisType(Enum):
    """
    Represents the type of analysis being performed.
    """
    SEMANTIC_RULES = 1,
    SEMANTIC_HINTS = 2,
    SEMANTIC_ALL = 3,
    EVIDENCE_QUALITY_ANALYSIS = 4
