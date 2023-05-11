from typing import Optional

from elements.flow_object.task.association import Association
from elements.element import Element


class PotentialEvidenceSource(Element):
    def __init__(self, elem_id, attached_to_ref, association=None):
        super().__init__(elem_id)

        self.attached_to_ref: str = attached_to_ref  # Union[FlowObject | DataStore]
        self.association: Optional[Association] = association
