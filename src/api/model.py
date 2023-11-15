
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class AnalysisType(str, Enum):
    SEMANTIC_RULES = 'SEMANTIC_RULES',
    SEMANTIC_HINTS = 'SEMANTIC_HINTS',
    SEMANTIC_ALL = 'SEMANTIC_ALL',
    EVIDENCE_QUALITY_ANALYSIS = 'EVIDENCE_QUALITY_ANALYSIS'

class AnalysisModel(BaseModel):
    model: str = Field(description="Base64-encoded XML model")
    analysis_type: AnalysisType 
    element_id: Optional[str] = Field(None, description="Element id_to analyse")
