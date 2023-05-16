from typing import Optional

from elements.element import Element


class Artefact(Element):
    """
    Represents a BPMN4FRSS Artefact.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for Artefact class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)

