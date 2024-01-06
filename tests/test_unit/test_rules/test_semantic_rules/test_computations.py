
from src.rules.rule_result.result import Result
from src.rules.semantic_rules.task_computations.keyed_hash_output import KeyedHashFunOutput
from src.rules.semantic_hints.computation_pes import ComputationPES
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

    expected_result = Result()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_integrity_computation_three_inputs(integrity_computation_three_inputs):
    rule = ComputationInput()
    result = rule.evaluate(integrity_computation_three_inputs)

    expected_result = Result()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

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

    expected_result = Result()
    expected_result.source = ["Task_14bpt81", "Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_all_computations_one_output(all_computations_one_input_output):
    rule = ComputationOutput()
    result = rule.evaluate(all_computations_one_input_output)

    assert result is None


def test_all_computations_bad_output_type(all_computations_bad_io_type):
    rule = ComputationOutput()
    result = rule.evaluate(all_computations_bad_io_type)

    expected_result = Result()
    expected_result.source = ["Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task performing a computation must have exactly one output, " \
                              "being a Potential Evidence."

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message
    

def test_all_computations_missing_pes(all_computations_one_input_output):
    rule = ComputationPES()
    result = rule.evaluate(all_computations_one_input_output)

    expected_result = Result()
    expected_result.source = ["Task_14bpt81", "Task_1mgfm3r", "Task_1qg7d8p"]
    expected_result.message = "Task performing computation should have a Potential Evidence Source label."

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message


def test_all_computations_with_pes(all_computations_with_pes):
    rule = ComputationPES()
    result = rule.evaluate(all_computations_with_pes)

    assert result is None


def test_keyed_hash_fun_output(keyed_hash_fun_input_output):
    rule = KeyedHashFunOutput()
    result = rule.evaluate(keyed_hash_fun_input_output)

    assert result is None


def test_keyed_hash_fun_bad_output(keyed_hash_fun_bad_input_output):
    rule = KeyedHashFunOutput()
    result = rule.evaluate(keyed_hash_fun_bad_input_output)

    expected_result = Result()
    expected_result.source = ["Activity_0aek6ep", "Activity_06q1s2x"]
    expected_result.message = "Task that executes the Keyed Hash Function must have exactly one output, " \
                              "Potential Evidence, being a Keyed Hash Proof."

    assert sorted(result.source) == sorted(expected_result.source) \
       and result.message == expected_result.message