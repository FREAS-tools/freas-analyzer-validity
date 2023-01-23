from typing import Optional

from elements.hash_function import HashFunction
from elements.flow_object.flow_object import FlowObject


class Task(FlowObject):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
        self.hash_fun: Optional[HashFunction] = None
