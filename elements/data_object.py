from elements.artefact import Artefact


class DataObject(Artefact):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class PotentialEvidenceType(DataObject):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class DataHash(DataObject):
    def __init__(self, elem_id):
        super().__init__(elem_id)
