from typing import Optional

from results.response import Response
from results.severity import Severity


class Mistake(Response):
    def __init__(self, message=""):
        super().__init__(message)
        self.severity: Optional[Severity] = None
