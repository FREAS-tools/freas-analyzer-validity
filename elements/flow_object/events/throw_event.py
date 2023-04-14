from elements.flow_object.events.event import Event


class ThrowEvent(Event):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class IntermediateThrowEvent(ThrowEvent):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class EndEvent(ThrowEvent):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
