from typing import Optional

from elements.artefact.artefact import Artefact


class DataObject(Artefact):
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)
        self.process_id = process_id


class PotentialEvidenceType(DataObject):
    def __init__(self, elem_id: str, process_id: str, name: Optional[str] = None):
        super().__init__(elem_id, process_id, name)
