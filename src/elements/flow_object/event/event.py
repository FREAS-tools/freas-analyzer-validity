from src.elements.flow_object.activity import Activity


class Event(Activity):
    """
    Represents a BPMN4FRSS Event element.
    """
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        """
        Constructor for Event class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance
        """
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
