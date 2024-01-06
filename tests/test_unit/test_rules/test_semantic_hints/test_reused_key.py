from src.rules.semantic_hints.reused_key import ReusedKey
from src.rules.rule_result.result import Result

def test_reused_key(keyed_hash_reused_key):
    rule = ReusedKey()
    result = rule.evaluate(keyed_hash_reused_key)

    expected_result = Result()
    expected_result.source = ["DataObject_1ntb5gz", "DataObject_01577su"]
    expected_result.message = "The key used in Keyed Hash Function must not be used in different Pool."

    assert isinstance(result, Result)
    assert sorted(result.source) == sorted(expected_result.source) \
           and result.message == expected_result.message


def test_unique_key_in_hash_fun(keyed_hash_fun_input_output):
    rule = ReusedKey()
    result = rule.evaluate(keyed_hash_fun_input_output)

    assert result is None
