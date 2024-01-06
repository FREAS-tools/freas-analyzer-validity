from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.analyzer.analyzer import Analyzer
from src.rules.rule_result.result import Result


def test_semantic_rules(integrity_computation_two_inputs):
    analysis_type = AnalysisType.SEMANTIC_RULES
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, integrity_computation_two_inputs)

    expected_result = Result()
    expected_result.source = ["Task_1e2yjs2"]
    expected_result.message = "Task performing a computation must have exactly one input, " \
                              "being a Potential Evidence Type."

    expected_output = Output()
    expected_output.errors = [expected_result]

    assert len(output.errors) == 1

    assert (sorted(expected_output.errors[0].source) == sorted(output.errors[0].source) and
            expected_output.errors[0].message == output.errors[0].message)
