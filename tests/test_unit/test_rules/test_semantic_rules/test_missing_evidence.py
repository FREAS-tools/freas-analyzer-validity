from src.rules.rule_result.result import Result
from src.rules.semantic_rules.missing_evidence import MissingPotentialEvidence


def test_has_potential_evidence(semantics_good_elements):
    rule = MissingPotentialEvidence()
    result = rule.evaluate(semantics_good_elements)

    assert result is None


def test_missing_potential_evidence(semantics_bad_elements):
    rule = MissingPotentialEvidence()
    result = rule.evaluate(semantics_bad_elements)

    expected_result = Result()
    expected_result.source = ["EvidenceSource_1i95iav"]
    expected_result.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message
