from elements.artefact import Artefact


class DataObject(Artefact):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class PotentialEvidenceType(DataObject):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class Proof(PotentialEvidenceType):
    def __init__(self, elem_id):
        super().__init__(elem_id)


class HashProof(Proof):
    def __init__(self, elem_id):
        super().__init__(elem_id)
        self.keyed: bool = False


class TimestampProof(Proof):
    def __init__(self, elem_id):
        super().__init__(elem_id)
