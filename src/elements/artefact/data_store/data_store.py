from typing import Optional

from src.elements.artefact.artefact import Artefact


class DataStore(Artefact):
    """
    Represents a BPMN4FRSS Data Store.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for DataStore class.
 
        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)
