from typing import Optional

from elements.element import Element


# participant
class Pool(Element):
    def __init__(self, elem_id: str, process_ref: str, name: Optional[str] = None):
        super().__init__(elem_id, name)
        self.process_ref: str = process_ref    # Process
