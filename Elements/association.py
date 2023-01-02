class Association:
    def __init__(self, source_ref, target_ref):
        self.source_ref: str = source_ref  # FlowObject | PotentialEvidenceSource
        self.target_ref: str = target_ref  # DataReference
