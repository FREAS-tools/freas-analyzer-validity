from src.rules.rule_result.result import Result 
from src.rules.semantic_hints.missing_pes import MissingPES


def test_missing_pes(missing_pes_elements):
    rule = MissingPES()
    result = rule.evaluate(missing_pes_elements)

    expected_result = Result()
    expected_result.source = ["Task_02p51vl", "IntermediateThrowEvent_0647pg8"]
    expected_result.message = "Flow Objects that are the source or target element of a Message Flow" \
                              " should have a Potential Evidence Source label."

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source) \
           and result.message == expected_result.message
