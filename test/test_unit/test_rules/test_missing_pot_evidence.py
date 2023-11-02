# from response.error import Error
#
# from rules.semantic_rules.missing_pot_evidence import MissingPotentialEvidence
# from fixtures.example_elements import semantics_good_elements, semantics_bad_elements
#
#
# def test_has_potential_evidence(semantics_good_elements):
#     rule = MissingPotentialEvidence()
#     result = rule.evaluate(semantics_good_elements)
#
#     assert result is None
#
#
# def test_hash_fun_missing_potential_evidence(semantics_bad_elements):
#     rule = MissingPotentialEvidence()
#     result = rule.evaluate(semantics_bad_elements)
#
#     expected_result = Error()
#     expected_result.source = ["PotentialEvidenceSource_1oqydbh"]
#     expected_result.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"
#
#     assert isinstance(result, Error)
#     assert sorted(result.source) == sorted(expected_result.source) \
#            and result.message == expected_result.message
