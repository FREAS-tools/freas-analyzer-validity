from elements.element import Element


class Flow(Element):
    def __init__(self, elem_id, elem_type, source_ref, target_ref, name=None):
        super().__init__(elem_id, elem_type, name)

        self.source_ref: str = source_ref   # Union[flow_object | Pool]
        self.target_ref: str = target_ref   # Union[flow_object | Pool]
