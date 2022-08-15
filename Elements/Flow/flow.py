from Elements.Element.element import Element


class Flow(Element):
    def __init__(self, elem_id, elem_type, source_ref, target_ref, name=None):
        super().__init__(elem_id, elem_type, name)
        self.source_ref: str = source_ref   # Union[FlowObject | Pool]
        self.target_ref: str = target_ref   # Union[FlowObject | Pool]
