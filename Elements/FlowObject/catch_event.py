from Elements.FlowObject.event import Event


class CatchEvent(Event):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)


class StartEvent(CatchEvent):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)


class IntermediateCatchEvent(CatchEvent):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)
