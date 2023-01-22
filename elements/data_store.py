from elements.artefact import Artefact


class DataStore(Artefact):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class EvidenceStore(DataStore):
    pass
