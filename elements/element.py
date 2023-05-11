from typing import Optional


class Element:
    def __init__(self, elem_id: str, name: Optional[str] = None):
        self.id: str = elem_id
        self.name: str = "" if name is None else name

