# from response.error import Error
#
# from rules.semantic_rules.hash_fun_pes import HashFunctionPES
# from fixtures.example_elements import hash_missing_pes_elements, hash_correct_pes_elements
#
#
# def test_hash_fun_has_pes(hash_correct_pes_elements):
#     rule = HashFunctionPES()
#     result = rule.evaluate(hash_correct_pes_elements)
#
#     assert result is None
#
#
# def test_hash_fun_missing_pes(hash_missing_pes_elements):
#     rule = HashFunctionPES()
#     result = rule.evaluate(hash_missing_pes_elements)
#
#     expected_result = Error()
#     expected_result.source = ["Activity_0l2nqgv"]
#     expected_result.message = "Tasks that execute (Keyed) Hash function must have Potential Evidence Source label"
#
#     assert isinstance(result, Error)
#     assert sorted(result.source) == sorted(expected_result.source) \
#            and result.message == expected_result.message
