from typing import Optional

from src.elements.artefact.data_object.pot_evidence_type import PotentialEvidenceType


class Proof(PotentialEvidenceType):
    """
    Represents a BPMN4FRSS Proof.
    """
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        """
        :param elem_id: element id
        :param process_id: Process id in which the Proof is created
        :param name: element name
        """
        super().__init__(elem_id, process_id, name)


class HashProof(Proof):
    """
    Represents a BPMN4FRSS Hash Proof.
    """
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        """
        Constructor for HashProof class.

        Parameters:
            elem_id (str): Element id
            process_id (str): Process id in which the Proof is created
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, process_id, name)


class KeyedHashProof(Proof):
    """
    Represents a BPMN4FRSS Keyed Hash Proof.
    """
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        """
        Constructor for KeyedHashProof class.

        Parameters:
            elem_id (str): Element id
            process_id (str): Process id in which the Proof is created
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, process_id, name)
