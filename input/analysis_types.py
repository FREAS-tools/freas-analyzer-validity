from enum import Enum


class AnalysisType(Enum):
    SEMANTIC_RULES = 1,
    SEMANTIC_HINTS = 2,
    SEMANTIC_ALL = 3,
    EVIDENCE_QUALITY_ANALYSIS = 4
