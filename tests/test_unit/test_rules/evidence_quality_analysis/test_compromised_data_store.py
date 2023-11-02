from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.response.response import Response


def test_compromised_data_store_no_pe(disputable_same_store_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_store_elements, "DataStoreReference_1qqlqq2")

    assert result is None


def test_compromised_data_store_has_pe(new_av_scenario):
    rule = CompromisedDataStore()
    result = rule.evaluate(new_av_scenario, "DataStoreReference_0a5zo83")

    expected_result = Response()
    expected_result.source = ["DataStore_0kxtat1"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)

