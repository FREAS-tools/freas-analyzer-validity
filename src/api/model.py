
from typing import Optional
from enum import Enum
from pydantic import BaseModel

class AnalysisType(str, Enum):
    SEMANTIC_RULES = 'SEMANTIC_RULES',
    SEMANTIC_HINTS = 'SEMANTIC_HINTS',
    SEMANTIC_ALL = 'SEMANTIC_ALL',
    EVIDENCE_QUALITY_ANALYSIS = 'EVIDENCE_QUALITY_ANALYSIS'

class AnalysisModel(BaseModel):
    model: str
    analysis_type: AnalysisType
    element_id: Optional[str]
