from typing import Optional

from src.elements.flow_object.activity import Activity
from src.elements.flow_object.hash_function import HashFunction


class Task(Activity):
    """
    Represents a task element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for Task class.

        Parameters:
            elem_id (str): element id
            name (str): element name
            incoming (str): incoming Flow object id
            outgoing (str): outgoing Flow object id
            pe_source (PotentialEvidenceSource): attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)

        self.hash_fun: Optional[HashFunction] = None
