from elements.flow_object.event.event import Event


class CatchEvent(Event):
    """
    Represents a BPMN4FRSS Catch Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for CatchEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class StartEvent(CatchEvent):
    """
    Represents a BPMN4FRSS Start Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for StartEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)


class IntermediateCatchEvent(CatchEvent):
    """
    Represents a BPMN4FRSS Intermediate Catch Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for IntermediateCatchEvent class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
