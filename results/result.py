from json import JSONEncoder
from typing import List, Optional

from results.error import BPMN4FRSSError
from results.warning import BPMN4FRSSWarning
from results.response import BPMN4FRSSResponse


class Result:
    def __init__(self):
        self.errors: List[BPMN4FRSSError] = []
        self.warnings: List[BPMN4FRSSWarning] = []
        self.evidence_sources: Optional[BPMN4FRSSResponse] = None


class ResultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
