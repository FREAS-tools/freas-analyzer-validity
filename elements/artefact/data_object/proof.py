from typing import Optional

from elements.artefact.data_object.data_object import PotentialEvidenceType


class Proof(PotentialEvidenceType):
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        super().__init__(elem_id, process_id, name)


class HashProof(Proof):
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        super().__init__(elem_id, process_id, name)


class KeyedHashProof(Proof):
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        super().__init__(elem_id, process_id, name)
