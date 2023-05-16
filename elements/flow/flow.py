from elements.element import Element


class Flow(Element):
    """
    Represents a BPMN4FRSS Flow between two Elements.
    """
    def __init__(self, elem_id, source_ref, target_ref, name=None):
        """
        Constructor for Flow class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Source element id
            target_ref (str): Target element id
            name (str): Element name
        """
        super().__init__(elem_id, name)

        self.source_ref: str = source_ref
        self.target_ref: str = target_ref
