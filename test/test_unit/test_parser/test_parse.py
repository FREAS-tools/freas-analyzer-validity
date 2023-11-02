import pytest

from src.elements.artefact.data_object.evidence_data_relation import EvidenceDataRelation
from src.elements.artefact.data_object.pot_evidence_type import PotentialEvidenceType
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.container.pool import Pool
from src.elements.container.process import Process
from src.elements.flow.message_flow import MessageFlow
from src.elements.flow.sequence_flow import SequenceFlow
from src.elements.flow_object.event.catch_event import StartEvent, IntermediateCatchEvent
from src.elements.flow_object.event.throw_event import EndEvent
from src.elements.flow_object.task.task import Task
from src.elements.pot_evidence_source import PotentialEvidenceSource


def test_parse(missing_pes_elements):
    # Test the parse function
    try:
        # elements = parse("../../../documentation/diagrams/missing_evidence_source.bpmn")
        elements = missing_pes_elements
        assert isinstance(elements, dict)
        # Add assertions for the expected elements of the parsing process
        assert len(elements) == 27

        # Assert the presence of specific keys and their corresponding value types in the elements dictionary
        assert "_6-1" in elements
        assert isinstance(elements["_6-1"], Process)

        assert "OrderReceivedEvent" in elements
        assert isinstance(elements["OrderReceivedEvent"], StartEvent)

        assert "Activity_0pfyvl2" in elements
        assert isinstance(elements["Activity_0pfyvl2"], Task)

        assert "Activity_1capgzc" in elements
        assert isinstance(elements["Activity_1capgzc"], Task)

        assert "Flow_0cnslyk" in elements
        assert isinstance(elements["Flow_0cnslyk"], SequenceFlow)

        assert "Flow_19smzqh" in elements
        assert isinstance(elements["Flow_19smzqh"], SequenceFlow)

        assert "Event_0fkz5kz" in elements
        assert isinstance(elements["Event_0fkz5kz"], EndEvent)

        assert "Flow_1s2vkd3" in elements
        assert isinstance(elements["Flow_1s2vkd3"], SequenceFlow)

        assert "PotentialEvidenceSource_1k4fys9" in elements
        assert isinstance(elements["PotentialEvidenceSource_1k4fys9"], PotentialEvidenceSource)

        assert "DataObjectReference_0imz72w" in elements
        assert isinstance(elements["DataObjectReference_0imz72w"], DataObjectReference)

        assert "DataObject_0aacclc" in elements
        assert isinstance(elements["DataObject_0aacclc"], PotentialEvidenceType)

        assert "_6-2" in elements
        assert isinstance(elements["_6-2"], Process)

        assert "_6-61" in elements
        assert isinstance(elements["_6-61"], StartEvent)

        assert "Activity_5capgzo" in elements
        assert isinstance(elements["Activity_5capgzo"], Task)

        assert "_6-125" in elements
        assert isinstance(elements["_6-125"], SequenceFlow)

        assert "Flow_1bnqw1s" in elements
        assert isinstance(elements["Flow_1bnqw1s"], SequenceFlow)

        assert "Flow_0s240ai" in elements
        assert isinstance(elements["Flow_0s240ai"], SequenceFlow)

        assert "Event_1o1itgk" in elements
        assert isinstance(elements["Event_1o1itgk"], IntermediateCatchEvent)

        assert "_6-406" in elements
        assert isinstance(elements["_6-406"], EndEvent)

        assert "PotentialEvidenceSource_1p0n1e7" in elements
        assert isinstance(elements["PotentialEvidenceSource_1p0n1e7"], PotentialEvidenceSource)

        assert "DataObjectReference_1oaappe" in elements
        assert isinstance(elements["DataObjectReference_1oaappe"], DataObjectReference)

        assert "DataObject_1dvjcrp" in elements
        assert isinstance(elements["DataObject_1dvjcrp"], PotentialEvidenceType)

        assert "_6-53" in elements
        assert isinstance(elements["_6-53"], Pool)

        assert "_6-438" in elements
        assert isinstance(elements["_6-438"], Pool)

        assert "_6-638" in elements
        assert isinstance(elements["_6-638"], MessageFlow)

        assert "Flow_0ju2vj0" in elements
        assert isinstance(elements["Flow_0ju2vj0"], MessageFlow)

        assert "EvidenceDataRelation_18psi5n" in elements
        assert isinstance(elements["EvidenceDataRelation_18psi5n"], EvidenceDataRelation)

    except Exception as e:
        pytest.fail(f"Error occurred while parsing XML: {e}")
