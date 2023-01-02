from elements.artefact import Artefact


class DataObject(Artefact):
    def __init__(self, elem_id, elem_type):
        super().__init__(elem_id, elem_type)


class PotentialEvidenceType(DataObject):
    def __init__(self, elem_id, elem_type):
        super().__init__(elem_id, elem_type)
