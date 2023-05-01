from typing import Optional

from results.response import BPMN4FRSSResponse
from results.severity import Severity


class BPMN4FRSSError(BPMN4FRSSResponse):
    def __init__(self, message="", severity: Optional[Severity] = None):
        super().__init__(message)
        self.severity: Optional[Severity] = severity
