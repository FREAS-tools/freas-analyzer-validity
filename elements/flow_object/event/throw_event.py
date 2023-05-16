from elements.flow_object.event.event import Event


class ThrowEvent(Event):
    """
    Represents a throw event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for ThrowEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class IntermediateThrowEvent(ThrowEvent):
    """
    Represents a BPMN4FRSS Intermediate Throw Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for IntermediateThrowEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class EndEvent(ThrowEvent):
    """
    Represents a BPMN4FRSS End Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for EndEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
