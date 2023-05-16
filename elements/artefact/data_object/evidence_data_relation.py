from elements.element import Element


class EvidenceDataRelation(Element):
    """
    Represents a BPMN4FRSS Evidence Data Relation.
    """
    def __init__(self, elem_id, source_ref, target_ref):
        """
        Constructor for EvidenceDataRelation class.

        Parameters:
            elem_id (str): Element id
            source_ref (str): Data Object Reference of a source Data Object
            target_ref (str): Data Object Reference of a target Data Object
        """
        super().__init__(elem_id)

        self.source_ref: str = source_ref
        self.target_ref: str = target_ref
