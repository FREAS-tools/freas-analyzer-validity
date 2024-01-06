from src.analyzer.analyzer import Analyzer
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.rules.rule_result.result import Result
from src.analysis_input.analysis_types import AnalysisType


def test_semantic_all_rules(av_parking_register):
    analysis_type = AnalysisType.SEMANTIC_ALL
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, av_parking_register)

    expected_result = Result()
    expected_result.source = ["Activity_0vqb0h1", "Event_1kwr4k9", "Activity_04iyke1", "Event_0e8vxiy"]
    expected_result.message = "Flow Objects that are the source or target element of a " \
                               "Message Flow should have a Potential Evidence Source label."

    expected_output = Output()
    expected_output.errors = [expected_result]

    assert len(output.errors) == 1

    assert (sorted(expected_output.errors[0].source) == sorted(output.errors[0].source) and
            expected_output.errors[0].message == output.errors[0].message)


def test_semantic_all_rules_1(integrity_computation_two_inputs):
    analysis_type = AnalysisType.SEMANTIC_ALL
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, integrity_computation_two_inputs)

    expected_result = Result()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing computation should have a Potential Evidence Source label."

    expected_result_1 = Result()
    expected_result_1.source = ["Task_1e2yjs2"]
    expected_result_1.message = "Task performing a computation must have exactly one input, " \
                                "being a Potential Evidence Type."

    expected_output = Output()
    expected_output.errors = [expected_result_1, expected_result]

    assert len(output.errors) == 2

    assert (sorted(expected_output.errors[0].source) == sorted(output.errors[0].source) and
            expected_output.errors[0].message == output.errors[0].message)
    
    assert (sorted(expected_output.errors[1].source) == sorted(output.errors[1].source) and
            expected_output.errors[1].message == output.errors[1].message)

