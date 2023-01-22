class Association:
    def __init__(self, source_ref, target_ref):
        self.source_ref: str = source_ref  # FlowObject | PotentialEvidenceSource
        self.target_ref: str = target_ref  # DataReference


class DataInputAssociation(Association):
    def __init__(self, source_ref, target_ref):
        super().__init__(source_ref, target_ref)


class DataOutputAssociation(Association):
    def __init__(self, source_ref, target_ref):
        super().__init__(source_ref, target_ref)
