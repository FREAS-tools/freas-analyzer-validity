from typing import Optional

from results.response import Response
from results.severity import Severity


class BPMN4FRSSError(Response):
    def __init__(self, message="", severity: Optional[Severity] = None):
        super().__init__(message)
        self.severity: Optional[Severity] = severity
