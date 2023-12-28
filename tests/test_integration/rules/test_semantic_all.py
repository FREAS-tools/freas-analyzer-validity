from src.rules.rule_result.error import Error
from src.rules.rule_result.warning import Warning
from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.analyzer.analyzer import Analyzer
from src.parser.parser import parse


def test_semantic_all_rules(av_parking_register):
    analysis_type = AnalysisType.SEMANTIC_ALL
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, av_parking_register)

    expected_warning = Warning()
    expected_warning.source = ["Activity_0vqb0h1", "Event_1kwr4k9", "Activity_04iyke1", "Event_0e8vxiy"]
    expected_warning.message = "Flow Objects that are the source or target element of a " \
                               "Message Flow should have a Potential Evidence Source label."

    expected_output = Output()
    expected_output.warnings = [expected_warning]

    assert len(output.warnings) == 1

    assert (sorted(expected_output.warnings[0].source) == sorted(output.warnings[0].source) and
            expected_output.warnings[0].message == output.warnings[0].message)


def test_semantic_all_rules_1(integrity_computation_two_inputs):
    analysis_type = AnalysisType.SEMANTIC_ALL
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, integrity_computation_two_inputs)

    expected_warning = Warning()
    expected_warning.source = ["Task_1e2yjs2"]
    expected_warning.message = "Task performing computation should have a Potential Evidence Source label."

    expected_error = Error()
    expected_error.source = ["Task_1e2yjs2"]
    expected_error.message = "Task performing a computation must have exactly one input, " \
                             "being a Potential Evidence Type."

    expected_output = Output()
    expected_output.errors = [expected_error]
    expected_output.warnings = [expected_warning]

    assert len(output.errors) == 1 and len(output.warnings) == 1

    assert (sorted(expected_output.errors[0].source) == sorted(output.errors[0].source) and
            expected_output.errors[0].message == output.errors[0].message)
    
    assert (sorted(expected_output.warnings[0].source) == sorted(output.warnings[0].source) and
            expected_output.warnings[0].message == output.warnings[0].message)
