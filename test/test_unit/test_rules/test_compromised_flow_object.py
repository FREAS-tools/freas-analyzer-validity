from rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from response.response import Response
from fixtures.example_elements import disputable_same_store_elements, disputable_same_context_elements


def test_compromised_flow_object_no_pe(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "Event_1i2umgm")

    assert result is None


def test_compromised_flow_object_has_pe(disputable_same_context_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_context_elements, "Activity_19xl907")

    expected_result = Response()
    expected_result.source = ["DataStore_mydatas"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)

