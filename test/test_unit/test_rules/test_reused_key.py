from rules.semantic_hints.reused_key import ReusedKey
from response.warning import Warning

from fixtures.example_elements import keyed_hash_reused_elements, keyed_hash_unique_elements


def test_reused_key_in_hash_fun(keyed_hash_reused_elements):
    rule = ReusedKey()
    result = rule.evaluate(keyed_hash_reused_elements)

    expected_result = Warning()
    expected_result.source = ["Participant_04cmj4g", "Participant_150mijc"]
    expected_result.message = "The key used in Keyed Hash Function must not be used in different Pool."

    assert isinstance(result, Warning)
    assert sorted(result.source) == sorted(expected_result.source) \
           and result.message == expected_result.message


def test_unique_key_in_hash_fun(keyed_hash_unique_elements):
    rule = ReusedKey()
    result = rule.evaluate(keyed_hash_unique_elements)

    assert result is None


