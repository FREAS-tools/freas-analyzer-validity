from elements.flow_object.flow_object import FlowObject


class Task(FlowObject):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name, incoming, outgoing, pe_source)
