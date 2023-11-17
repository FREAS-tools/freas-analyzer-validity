from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.rules.rule_result.result import Result


def test_compromised_data_store_no_pe(disputable_same_store_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_store_elements, "DataStoreReference_0zf3t9g")

    assert result is None


def test_compromised_data_store_has_pe(disputable_same_context_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_context_elements, "DataStoreReference_0i2rn37")

    expected_result = Result()
    expected_result.source = ["DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)
