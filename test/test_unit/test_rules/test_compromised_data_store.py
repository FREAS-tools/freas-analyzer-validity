from rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from response.response import Response
from fixtures.example_elements import disputable_same_store_elements, disputable_same_context_elements


def test_compromised_data_store_no_pe(disputable_same_store_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_store_elements, "DataStoreReference_1qqlqq2")

    assert result is None


def test_compromised_data_store_has_pe(disputable_same_context_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_context_elements, "DataStoreReference_1qqlqq2")

    expected_result = Response()
    expected_result.source = ["DataStore_mydatas"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)

