from typing import Optional


class Element:
    """
    Base class for all BPMN4FRSS elements in the model.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for Element class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        self.id: str = elem_id
        self.name: str = "" if name is None else name

