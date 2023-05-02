from typing import List, Optional


class BPMN4FRSSResponse:
    def __init__(self, message: str = "", source: Optional[List[str]] = None):
        self.source: List[str] = source if source is not None else []
        self.message: str = message
