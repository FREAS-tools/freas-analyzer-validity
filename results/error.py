from typing import Optional, List

from results.response import BPMN4FRSSResponse
from results.severity import Severity


class BPMN4FRSSError(BPMN4FRSSResponse):
    def __init__(self, message: str = "", source: Optional[List[str]] = None, severity: Optional[Severity] = None):
        super().__init__(message, source)
        self.severity: Optional[Severity] = severity
