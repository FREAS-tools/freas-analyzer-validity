from typing import Optional, List

from result.response import BPMN4FRSSResponse
from result.severity import Severity


class BPMN4FRSSError(BPMN4FRSSResponse):
    def __init__(self, message: str = "", source: Optional[List[str]] = None, severity: Optional[Severity] = None):
        super().__init__(message, source)
        self.severity: Optional[Severity] = severity
