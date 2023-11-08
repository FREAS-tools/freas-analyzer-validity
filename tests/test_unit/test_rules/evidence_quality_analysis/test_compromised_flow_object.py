from src.rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from src.response.response import Response


def test_compromised_flow_object_no_pe(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "StartEvent_1v6nqn7")

    assert result is None


def test_compromised_flow_object_has_pe(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "Task_0pcmu9v")

    expected_result = Response()
    expected_result.source = ["DataStore_0zf3t9g"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_flow_object_has_pe_1(disputable_same_context_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_context_elements, "Task_0pcmu9v")

    expected_result = Response()
    expected_result.source = ["DataStore_1t4979h"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)
