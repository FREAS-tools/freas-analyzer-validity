from elements.element import Element


class Association(Element):
    """
    Represents an BPMN4FRSS Association between two elements.
    """
    def __init__(self, elem_id, source_ref, target_ref):
        """
        Constructor for Association class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Source element id
            target_ref (str): Target element id
        """
        super().__init__(elem_id)

        self.source_ref: str = source_ref
        self.target_ref: str = target_ref


class DataInputAssociation(Association):
    """
    Represents a BPMN4FRSS Data Input Association between two Elements.
    """
    def __init__(self, elem_id, source_ref, target_ref):
        """
        Constructor for DataInputAssociation class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Data Object id
            target_ref (str): Element id
        """
        super().__init__(elem_id, source_ref, target_ref)


class DataOutputAssociation(Association):
    """
    Represents a BPMN4FRSS Data Output Association between two elements.
    """
    def __init__(self, elem_id, source_ref, target_ref):
        """
        Constructor for DataOutputAssociation class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Element id
            target_ref (str): Data Object id
        """
        super().__init__(elem_id, source_ref, target_ref)
