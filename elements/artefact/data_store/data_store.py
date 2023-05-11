from typing import List, Optional

from elements.artefact.artefact import Artefact


class DataStore(Artefact):
    def __init__(self, elem_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)
        self.stored_pe: List[str] = []  # list of DataObjects
