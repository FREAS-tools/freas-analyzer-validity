from Elements.Flow.flow import Flow


class SequenceFlow(Flow):
    def __init__(self, elem_id, elem_type, source_ref, target_ref, name=None):
        super().__init__(elem_id, elem_type, source_ref, target_ref, name)
