from typing import Optional

from src.elements.flow_object.task.association import Association
from src.elements.element import Element


class PotentialEvidenceSource(Element):
    """
    Represents a BPMN4FRSS Potential Evidence Source.
    """
    def __init__(self, elem_id, attached_to_ref, association=None):
        """
        Constructor for PotentialEvidenceSource class.

        Parameters:
            elem_id (str): Element id
            attached_to_ref (str): Activity id
            association (Association): Association between the source and Data Object,
            representing a potential evidence
        """
        super().__init__(elem_id)

        self.attached_to_ref: str = attached_to_ref
        self.association: Optional[Association] = association
