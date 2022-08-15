from typing import Optional

from Elements.Element.element import Element


# abstract?
class FlowObject(Element):
    def __init__(self, elem_id, elem_type, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, elem_type, name)
        self.incoming: str = incoming   # Optional[Flow]
        self.outgoing: str = outgoing   # Optional[Flow]

        from Elements.PESource.pe_source import PotentialEvidenceSource

        self.pe_source: Optional[PotentialEvidenceSource] = pe_source
