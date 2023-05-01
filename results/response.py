from typing import List


class BPMN4FRSSResponse:
    def __init__(self, message=""):
        self.source: List[str] = []
        self.message: str = message
