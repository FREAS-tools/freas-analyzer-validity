from typing import List, Optional

from result.response import BPMN4FRSSResponse


class BPMN4FRSSWarning(BPMN4FRSSResponse):
    def __init__(self, message: str = "", source: Optional[List[str]] = None,):
        super().__init__(message, source)
