from elements.element import Element


class EvidenceDataRelation(Element):
    def __init__(self, elem_id, elem_type, source_ref, target_ref):
        super().__init__(elem_id, elem_type)
        self.source_ref: str = source_ref  # DataObjectReference
        self.target_ref: str = target_ref  # DataObjectReference
