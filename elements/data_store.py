from typing import List

from elements.artefact import Artefact


class DataStore(Artefact):
    def __init__(self, elem_id):
        super().__init__(elem_id)
        self.stored_pe: List[str] = []  # list of DataObjects


class EvidenceStore(DataStore):
    pass
