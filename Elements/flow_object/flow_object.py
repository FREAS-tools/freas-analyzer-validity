from typing import Optional

from elements.element import Element
from elements.pe_source import PotentialEvidenceSource


class FlowObject(Element):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name)
        self.incoming: str = incoming   # Optional[Flow]
        self.outgoing: str = outgoing   # Optional[Flow]
        self.pe_source: Optional[PotentialEvidenceSource] = pe_source
