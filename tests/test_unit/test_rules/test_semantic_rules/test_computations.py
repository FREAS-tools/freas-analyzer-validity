
from src.rules.rule_result.error import Error
from rules.semantic_rules.computation_input import ComputationInput


def test_integrity_computation_one_input(integrity_computation_one_input):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_one_input)

    assert result is None


def test_integrity_computation_two_inputs(integrity_computation_two_inputs):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_two_inputs)

    expected_result = Error()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task that performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_integrity_computation_three_inputs(integrity_computation_three_inputs):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_three_inputs)

    expected_result = Error()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task that performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_all_computations_one_input_output(all_computations_one_input_output):
    rule = ComputationInput()
    result = rule.evaluate(all_computations_one_input_output)

    assert result is None


def test_all_computations_bad_input_type(all_computations_bad_input_type):
    rule = ComputationInput()
    result = rule.evaluate(all_computations_bad_input_type)

    expected_result = Error()
    expected_result.source = ["Task_14bpt81", "Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task that performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message
