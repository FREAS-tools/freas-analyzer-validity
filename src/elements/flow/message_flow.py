from src.elements.flow.flow import Flow


class MessageFlow(Flow):
    """
    Represents a BPMN4FRSS Message Flow between two Elements.
    """
    def __init__(self, elem_id, source_ref, target_ref, name=None):
        """
        Constructor for MessageFlow class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Source element id
            target_ref (str): Target element id
            name (str): Element name
        """
        super().__init__(elem_id, source_ref, target_ref, name)
