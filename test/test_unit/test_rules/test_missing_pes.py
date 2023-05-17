from rules.semantic_hints.missing_pes import MissingPES
from response.warning import Warning

from fixtures.example_elements import missing_pes_elements


def test_missing_pes(missing_pes_elements):
    rule = MissingPES()
    result = rule.evaluate(missing_pes_elements)

    expected_result = Warning()
    expected_result.source = ["Activity_1capgzc", "Event_1o1itgk"]
    expected_result.message = "Flow Objects that are the source or target element of a Message Flow" \
                              " should have a Potential Evidence Source label"

    assert isinstance(result, Warning)
    assert sorted(result.source) == sorted(expected_result.source) \
           and result.message == expected_result.message
