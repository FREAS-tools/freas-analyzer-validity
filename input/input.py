from typing import Optional

from input.analysis_types import AnalysisType


class Input:
    """
    Represents an Input for the analysis.
    """
    def __init__(self, analysis_type, element_id: Optional[str] = None):
        """
        Constructor for Input class.

        Parameters:
            analysis_type (AnalysisType): Type of analysis being performed
            element_id (Optional[str]): In case of Evidence Quality analysis was chosen,
                the element id of the selected Data Object or Data Store
        """
        self.analysis_type: AnalysisType = analysis_type
        self.element_id: Optional[str] = element_id
