
from src.rules.rule_result.error import Error
from src.rules.semantic_rules.task_computations.computation_pes import ComputationPES
from src.rules.semantic_rules.task_computations.computation_input import ComputationInput
from src.rules.semantic_rules.task_computations.computation_output import ComputationOutput
from src.rules.semantic_rules.task_computations.integrity_computation_output import IntegrityComputationOutput


def test_integrity_computation_one_input(integrity_computation_one_input):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_one_input)

    assert result is None


def test_integrity_computation_two_inputs(integrity_computation_two_inputs):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_two_inputs)

    expected_result = Error()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_integrity_computation_three_inputs(integrity_computation_three_inputs):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_three_inputs)

    expected_result = Error()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_integrity_computation_output_good(integrity_computation_output_good):
    rule = IntegrityComputationOutput()
    result = rule.evaluate(integrity_computation_output_good)

    assert result is None


def test_all_computations_one_input(all_computations_one_input_output):
    rule = ComputationInput()
    result = rule.evaluate(all_computations_one_input_output)

    assert result is None


def test_all_computations_bad_input_type(all_computations_bad_io_type):
    rule = ComputationInput()
    result = rule.evaluate(all_computations_bad_io_type)

    expected_result = Error()
    expected_result.source = ["Task_14bpt81", "Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_all_computations_one_output(all_computations_one_input_output):
    rule = ComputationOutput()
    result = rule.evaluate(all_computations_one_input_output)

    assert result is None


def test_all_computations_bad_output_type(all_computations_bad_io_type):
    rule = ComputationOutput()
    result = rule.evaluate(all_computations_bad_io_type)

    expected_result = Error()
    expected_result.source = ["Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task performing a computation must have exactly one output, " \
                              "being a Potential Evidence."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message
    

def test_all_computations_missing_pes(all_computations_one_input_output):
    rule = ComputationPES()
    result = rule.evaluate(all_computations_one_input_output)

    expected_result = Error()
    expected_result.source = ["Task_14bpt81", "Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Computation tasks must have Potential Evidence Source label."

    assert isinstance(result, Error)
    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_all_computations_with_pes(all_computations_with_pes):
    rule = ComputationPES()
    result = rule.evaluate(all_computations_with_pes)

    assert result is None