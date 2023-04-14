from typing import Optional, List

from elements.element import Element
from elements.pe_source import PotentialEvidenceSource
from elements.data_association import DataOutputAssociation, DataInputAssociation


class FlowObject(Element):
    def __init__(self, elem_id, name, incoming, outgoing, pe_source):
        super().__init__(elem_id, name)
        self.incoming: str = incoming   # Optional[Flow]
        self.outgoing: str = outgoing   # Optional[Flow]
        self.pe_source: Optional[PotentialEvidenceSource] = pe_source
        self.data_output: List[DataOutputAssociation] = []
        self.data_input: List[DataInputAssociation] = []
