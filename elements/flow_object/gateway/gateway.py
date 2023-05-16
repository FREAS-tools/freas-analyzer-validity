from typing import List, Optional

from elements.flow_object.flow_object import FlowObject


class Gateway(FlowObject):
    """
    Represents a BPMN4FRSS Gateway element.
    Contains the id, name, incoming and outgoing flows (Sequence Flows).
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for Gateway class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)

        self.incoming: List[str] = []
        self.outgoing: List[str] = []


class ExclusiveGateway(Gateway):
    """
    Represents an BPMN4FRSS Exclusive Gateway element.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for ExclusiveGateway class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)


class ParallelGateway(Gateway):
    """
    Represents a BPMN4FRSS Parallel Gateway element.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for ParallelGateway class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)
