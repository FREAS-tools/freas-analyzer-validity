from src.rules.semantic_hints.missing_pes import MissingPES
from src.rules.rule_result.result import Result
from src.rules.semantic_rules.missing_evidence import MissingPotentialEvidence
from src.rules.semantic_hints.different_evidence_context import DiffEvidenceContext


def test_missing_evidence(demo):
    rule = MissingPotentialEvidence()
    result = rule.evaluate(demo)

    expected_result = Result()
    expected_result.source = ["EvidenceSource_0naeosx"]
    expected_result.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_missing_pes(demo):
    rule = MissingPES()
    result = rule.evaluate(demo)

    expected_warning = Result()
    expected_warning.source = ["DataObject_0puktn2"]
    expected_warning.message = "Potential Evidence should have a Potential Evidence Source."

    assert result.source == expected_warning.source \
         and result.message == expected_warning.message


def test_diff_ev_context(demo):
    rule = DiffEvidenceContext()
    result = rule.evaluate(demo)

    expected_result = Result()
    expected_result.source = ["DataObject_0bpfd4d", "DataObject_0mow4l3"]

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source)
