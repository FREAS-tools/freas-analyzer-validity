from typing import Optional

from elements.association import Association
from elements.element import Element


class PotentialEvidenceSource(Element):
    def __init__(self, elem_id, elem_type, attached_to_ref, association=None):
        super().__init__(elem_id, elem_type)

        self.attached_to_ref: str = attached_to_ref  # Union[FlowObject | DataStore]
        self.association: Optional[Association] = association
