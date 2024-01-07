from src.rules.rule_result.result import Result
from src.rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore


def test_rics_issuing_permit(rics_issuing_permit):
    rule = CompromisedFlowObject()
    result = rule.evaluate(rics_issuing_permit, "IntermediateThrowEvent_0qu79dp")

    assert result is None


def test_rics_issuing_permit_reservation_storage(rics_issuing_permit_reservation_storage):
    rule = CompromisedFlowObject()
    result = rule.evaluate(rics_issuing_permit_reservation_storage, "IntermediateThrowEvent_0qu79dp")

    expected_result = Result()
    expected_result.source = ["DataStore_0261slf"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)

def test_compromised_rics_issuing_permit_same_store(rics_issuing_permit):
    rule = CompromisedDataStore()
    result = rule.evaluate(rics_issuing_permit, "DataStoreReference_1o9b6q1")

    expected_result = Result()
    expected_result.source = ["DataStore_0cc7owv"]

    assert result is None


def test_compromised_rics_issuing_permit_log_storage(rics_issuing_permit_log_storage):
    rule = CompromisedDataStore()
    result = rule.evaluate(rics_issuing_permit_log_storage, "DataStoreReference_1o9b6q1")

    expected_result = Result()
    expected_result.source = ["DataStore_0p4so33"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


