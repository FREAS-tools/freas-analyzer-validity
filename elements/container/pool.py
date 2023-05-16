from typing import Optional

from elements.element import Element


# participant
class Pool(Element):
    """
    Represents a BPMN4FRSS Participant.
    """
    def __init__(self, elem_id: str, process_ref: str, name: Optional[str] = None):
        """
        Constructor for Pool class.

        Parameters:
            elem_id (str): Element id
            process_ref (str): id of the Process
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)
        self.process_ref: str = process_ref    # Process
