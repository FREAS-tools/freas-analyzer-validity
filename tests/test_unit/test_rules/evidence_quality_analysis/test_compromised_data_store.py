from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.rules.rule_result.result import Result


def test_compromised_data_store_no_pe(disputable_same_store_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_store_elements, "DataStoreReference_0zf3t9g")

    assert result is None


def test_compromised_data_store_no_pe_1(disputable_same_context_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_context_elements, "DataStoreReference_1t4979h")

    expected_result = Result()
    expected_result.source = ["DataStore_0i2rn37"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_data_store_has_pe(disputable_same_context_elements):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_same_context_elements, "DataStoreReference_0i2rn37")

    expected_result = Result()
    expected_result.source = ["DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_disputable_stored_on_user_device_two_pe(disputable_stored_on_user_device):
    rule = CompromisedDataStore()
    result = rule.evaluate(disputable_stored_on_user_device, "DataStoreReference_119fei9")

    expected_result = Result()
    expected_result.source = ["DataStore_0i2rn37", "DataStore_1t4979h"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_data_store(evidence_quality):
    rule = CompromisedDataStore()
    result = rule.evaluate(evidence_quality, "DataStoreReference_1hirzlo")

    expected_result = Result()
    expected_result.source = ["DataStore_1bfgusl", "DataStore_1b4kf8o"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_data_store_1(evidence_quality):
    rule = CompromisedDataStore()
    result = rule.evaluate(evidence_quality, "DataStoreReference_07m6ipb")

    expected_result = Result()
    expected_result.source = ["DataStore_0qiobg1", "DataStore_1b4kf8o"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_compromised_data_store_2(evidence_quality):
    rule = CompromisedDataStore()
    result = rule.evaluate(evidence_quality, "DataStoreReference_105pkxv")

    expected_result = Result()
    expected_result.source = ["DataStore_0qiobg1", "DataStore_1bfgusl"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_different_evidence_context(different_evidence_context):
    rule = CompromisedDataStore()
    result = rule.evaluate(different_evidence_context, "DataStoreReference_0fwvl82")

    expected_result = Result()
    expected_result.source = ["DataStore_0csaguc"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_different_evidence_context_1(different_evidence_context):
    rule = CompromisedDataStore()
    result = rule.evaluate(different_evidence_context, "DataStoreReference_0me5nk0")

    expected_result = Result()
    expected_result.source = ["DataStore_0gfsmzy"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_av_parking_register(av_parking_register):
    rule = CompromisedDataStore()
    result = rule.evaluate(av_parking_register, "DataStoreReference_1xrs3gb")

    expected_result = Result()
    expected_result.source = ["DataStore_0f64bhv"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


def test_av_parking_register_different_context(av_parking_register):
    rule = CompromisedDataStore()
    result = rule.evaluate(av_parking_register, "DataStoreReference_0b04ko3")

    expected_result = Result()
    expected_result.source = ["DataStore_0h5q69s"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)
