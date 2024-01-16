from src.rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from src.rules.rule_result.result import Result


def test_compromised_flow_object_no_pe(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "StartEvent_1v6nqn7")

    assert result is None


def test_compromised_flow_object_no_pe_1(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "Task_1was29v")

    assert result is None


def test_compromised_flow_object_has_pe(disputable_same_store_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_store_elements, "Task_0pcmu9v")

    expected_result = Result()
    expected_result.source = ["DataStore_0zf3t9g"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_flow_object_has_pe_1(disputable_same_context_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_context_elements, "Task_0pcmu9v")

    expected_result = Result()
    expected_result.source = ["DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_flow_object_has_pe_2(disputable_same_context_elements):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_same_context_elements, "Task_1o3t9qk")

    expected_result = Result()
    expected_result.source = ["DataStore_1t4979h", "DataStore_0i2rn37"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_disputable_on_user_device_no_pe(disputable_stored_on_user_device):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_stored_on_user_device, "EndEvent_14wpah1")

    assert result is None


def test_disputable_on_user_device(disputable_stored_on_user_device):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_stored_on_user_device, "Task_0pzke0h")

    expected_result = Result()
    expected_result.source = ["DataStore_0i2rn37", "DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_disputable_on_user_device_1(disputable_stored_on_user_device):
    rule = CompromisedFlowObject()
    result = rule.evaluate(disputable_stored_on_user_device, "IntermediateThrowEvent_1twbc5b")

    expected_result = Result()
    expected_result.source = ["DataStore_0i2rn37", "DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_flow_object(evidence_quality):
    rule = CompromisedFlowObject()
    result = rule.evaluate(evidence_quality, "Task_1t8os0h")

    expected_result = Result()
    expected_result.source = ["DataStore_0qiobg1"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_flow_object_1(evidence_quality):
    rule = CompromisedFlowObject()
    result = rule.evaluate(evidence_quality, "Task_1gtz9f7")

    expected_result = Result()
    expected_result.source = ["DataStore_0qiobg1", "DataStore_1bfgusl"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_different_evidence_context(different_evidence_context):
    rule = CompromisedFlowObject()
    result = rule.evaluate(different_evidence_context, "Activity_1w16j14")

    expected_result = Result()
    expected_result.source = ["DataStore_0gfsmzy"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_different_evidence_context_1(different_evidence_context):
    rule = CompromisedFlowObject()
    result = rule.evaluate(different_evidence_context, "Activity_1kop5s6")

    assert result is None


def test_av_parking_register(av_parking_register):
    rule = CompromisedFlowObject()
    result = rule.evaluate(av_parking_register, "Activity_0vqb0h1")

    assert result is None


def test_av_parking_register_1(av_parking_register):
    rule = CompromisedFlowObject()
    result = rule.evaluate(av_parking_register, "Activity_04iyke1")

    expected_result = Result()
    expected_result.source = ["DataStore_0h5q69s"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_av_parking_register_2(av_parking_register):
    rule = CompromisedFlowObject()
    result = rule.evaluate(av_parking_register, "Activity_15t262y")

    expected_result = Result()
    expected_result.source = ["DataStore_0h5q69s"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_before_after(before_after):
    rule = CompromisedFlowObject()
    result = rule.evaluate(before_after, "Activity_0vqb0h1")

    expected_result = Result()
    expected_result.source = ["DataStore_121kzwk"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_before_after_1(before_after):
    rule = CompromisedFlowObject()
    result = rule.evaluate(before_after, "Activity_161mmal")

    expected_result = Result()
    expected_result.source = ["DataStore_121kzwk", "DataStore_0qduasf"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)
