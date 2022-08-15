from typing import Optional, Union

from Elements.Association.association import Association
from Elements.Element.element import Element


class PotentialEvidenceSource(Element):
    def __init__(self, elem_id, elem_type, attached_to_ref, association=None):
        super().__init__(elem_id, elem_type)
        self.attached_to_ref: str = attached_to_ref  # Union[FlowObject | Artefact]
        self.association: Optional[Association] = association
