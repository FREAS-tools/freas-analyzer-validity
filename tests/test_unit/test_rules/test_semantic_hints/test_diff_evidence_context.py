from src.rules.rule_result.result import Result
from src.rules.semantic_hints.different_evidence_context import HashDiffEvidenceContext

def test_diff_ev_context(diff_evidence_context):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(diff_evidence_context)

    assert result is None


def test_diff_ev_context_1(av_scenario):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(av_scenario)

    assert result is None


# Same context different data store
def test_same_ev_context(same_evidence_context):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(same_evidence_context)

    expected_result = Result()
    expected_result.source = ["DataObject_1eiynzk", "DataObject_0fxl70a"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


# No data store
def test_ev_not_stored(integrity_computation):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(integrity_computation)

    expected_result = Result()
    expected_result.source = ["DataObject_1eiynzk", "DataObject_023u89c"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


# Same evidence store
def test_same_ev_store(same_evidence_store):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(same_evidence_store)

    expected_result = Result()
    expected_result.source = ["DataObject_1eiynzk", "DataObject_0fxl70a"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)

    
# one stored other not
def test_one_evidence_stored(one_evidence_stored):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(one_evidence_stored)

    expected_result = Result()
    expected_result.source = ["DataObject_1eiynzk", "DataObject_0fxl70a"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)


# Two computations: one good, one bad
def test_two_computations(evidence_context):
    rule = HashDiffEvidenceContext()
    result = rule.evaluate(evidence_context)

    expected_result = Result()
    expected_result.source = ["DataObject_062151r", "DataObject_125o9yx"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)