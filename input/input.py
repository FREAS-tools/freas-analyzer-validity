from typing import Optional

from input.analysis_types import AnalysisType


class BPMN4FRSSInput:
    def __init__(self, analysis_type, element_id: Optional[str] = None):
        self.analysis_type: AnalysisType = analysis_type
        self.element_id: Optional[str] = element_id
