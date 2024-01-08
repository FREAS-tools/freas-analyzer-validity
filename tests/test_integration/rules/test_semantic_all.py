from src.analyzer.analyzer import Analyzer
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.analyzer.analyzer import Analyzer
from src.rules.rule_result.result import Result
from src.analysis_input.analysis_types import AnalysisType


def test_semantic_all_rules(integrity_computation_two_inputs):
    analysis_type = AnalysisType.SEMANTIC_ALL
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, integrity_computation_two_inputs)

    expected_warning_1 = Result()
    expected_warning_1.source = ["DataObject_1g6i2ep", "DataObject_0oemdf4"]
    expected_warning_1.message = "Potential Evidence should have a Potential Evidence Source."

    expected_warning_2 = Result()
    expected_warning_2.source = ["Task_1e2yjs2"]
    expected_warning_2.message = "Task performing computation should have a Potential Evidence Source label."

    expected_error = Result()
    expected_error.source = ["Task_1e2yjs2"]
    expected_error.message = "Task performing a computation must have exactly one input, " \
                             "being a Potential Evidence Type."

    expected_output = Output()
    expected_output.errors = [expected_error]
    expected_output.warnings = [expected_warning_1, expected_warning_2]

    assert len(output.errors) == 1 and len(output.warnings) == 2

    assert (sorted(expected_output.errors[0].source) == sorted(output.errors[0].source) and
            expected_output.errors[0].message == output.errors[0].message)
    
    assert (sorted(expected_output.warnings[0].source) == sorted(output.warnings[0].source) and
            expected_output.warnings[0].message == output.warnings[0].message)
    
    assert (sorted(expected_output.warnings[1].source) == sorted(output.warnings[1].source) and
            expected_output.warnings[1].message == output.warnings[1].message)
