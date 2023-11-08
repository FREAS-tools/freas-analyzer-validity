from typing import Optional

from src.elements.artefact.artefact import Artefact


class DataObject(Artefact):
    """
    Represents a BPMN4FRSS Data Object.
    """
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        """
        Constructor for DataObject class.

        Parameters:
            elem_id (str): Element id
            process_id (str): Process id in which the Data Object is created
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)
        self.process_id = process_id
