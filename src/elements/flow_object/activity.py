from typing import Optional, List

from src.elements.flow_object.flow_object import FlowObject
from src.elements.pot_evidence_source import PotentialEvidenceSource
from src.elements.flow_object.task.association import DataOutputAssociation, DataInputAssociation


class Activity(FlowObject):
    """
    Represents an BPMN4FRSS Activity.
    """
    def __init__(self, elem_id, name, incoming, outgoing, pe_source):
        """
        Constructor for Activity class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
            incoming (str): Incoming Flow object id
            outgoing (str): Outgoing Flow object id
            pe_source (PotentialEvidenceSource): Attached PotentialEvidenceSource instance

        data_input (List[DataInputAssociation]): List of DataInputAssociation instances
        data_output (List[DataOutputAssociation]): List of DataOutputAssociation instances
        """
        super().__init__(elem_id, name)

        self.incoming: str = incoming
        self.outgoing: str = outgoing
        self.pe_source: Optional[PotentialEvidenceSource] = pe_source
        self.data_input: List[DataInputAssociation] = []
        self.data_output: List[DataOutputAssociation] = []
