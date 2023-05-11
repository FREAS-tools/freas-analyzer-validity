from typing import Optional

from elements.element import Element


class Artefact(Element):
    def __init__(self, elem_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)

