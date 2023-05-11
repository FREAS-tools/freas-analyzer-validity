from elements.element import Element


class EvidenceDataRelation(Element):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id)
        self.source_ref: str = source_ref  # DataObjectReference
        self.target_ref: str = target_ref  # DataObjectReference
