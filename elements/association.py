from elements.element import Element


class Association:
    def __init__(self, source_ref, target_ref):
        self.source_ref: str = source_ref  # FlowObject | PotentialEvidenceSource
        self.target_ref: str = target_ref  # DataReference


class DataAssociation(Element):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id)
        self.source_ref: str = source_ref  # FlowObject | PotentialEvidenceSource
        self.target_ref: str = target_ref  # DataReference


class DataInputAssociation(DataAssociation):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id, source_ref, target_ref)


class DataOutputAssociation(DataAssociation):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id, source_ref, target_ref)
