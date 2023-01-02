from elements.flow_object.event import Event


class ThrowEvent(Event):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)


class IntermediateThrowEvent(ThrowEvent):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)


class EndEvent(ThrowEvent):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)
