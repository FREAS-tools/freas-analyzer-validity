from elements.element import Element


class DataAssociation(Element):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id)
        self.source_ref: str = source_ref
        self.target_ref: str = target_ref


class DataInputAssociation(DataAssociation):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id, source_ref, target_ref)


class DataOutputAssociation(DataAssociation):
    def __init__(self, elem_id, source_ref, target_ref):
        super().__init__(elem_id, source_ref, target_ref)
