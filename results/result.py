from typing import List

from results.error import BPMN4FRSSError
from results.warning import BPMN4FRSSWarning
from results.response import Response


class Result:
    def __init__(self):
        self.errors: List[BPMN4FRSSError] = []
        self.warnings: List[BPMN4FRSSWarning] = []
        self.evidence_stores: List[Response] = []
