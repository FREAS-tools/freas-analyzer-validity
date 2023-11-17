from typing import Optional

from src.elements.artefact.data_object.data_object import DataObject


class PotentialEvidenceType(DataObject):
    """
    Represents a BPMN4FRSS Potential Evidence Type.
    """
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        """
        Constructor for PotentialEvidenceType class.

        Parameters:
            elem_id (str): Element id
            process_id (str): Process id in which the Data Object is created
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, process_id, name)
