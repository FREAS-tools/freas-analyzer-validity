from elements.flow_object.flow_object import FlowObject


class Event(FlowObject):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
