from typing import List, Optional

from elements.flow_object.flow_object import FlowObject


class Gateway(FlowObject):
    def __init__(self, elem_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)
        self.incoming: List[str] = []  # SequenceFlow
        self.outgoing: List[str] = []  # SequenceFlow


class ExclusiveGateway(Gateway):
    def __init__(self, elem_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)


class ParallelGateway(Gateway):
    def __init__(self, elem_id: str, name: Optional[str] = None):
        super().__init__(elem_id, name)
