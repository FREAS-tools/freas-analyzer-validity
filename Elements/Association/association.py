class Association:
    def __init__(self, source_ref, target_ref):
        from Elements.PESource.pe_source import PotentialEvidenceSource

        self.source_ref: str = source_ref  # FlowObject | PotentialEvidenceSource
        self.target_ref: str = target_ref  # DataObjectReference
