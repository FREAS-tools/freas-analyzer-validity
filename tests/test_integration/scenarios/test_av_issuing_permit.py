from src.rules.rule_result.result import Result
from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.analyzer.analyzer import Analyzer


def test_av_issuing_permit(av_issuing_permit):
    analysis_type = AnalysisType.SEMANTIC_HINTS
    analysis_input = Input(analysis_type, None)

    output = Analyzer.analyze(analysis_input, av_issuing_permit)

    expected_result = Result()
    expected_result.source = ["Task_08a6fnx", "StartEvent_0qnzcti", "Task_1abj0j9", "IntermediateThrowEvent_02t9brc",
                               "Task_1pph5kb", "IntermediateThrowEvent_00nrwm5", "Task_0rgnk7g", "IntermediateThrowEvent_0r56d1n",
                               "Task_0tqkd41", "IntermediateThrowEvent_0u17fz0", "Task_099wjuv", "IntermediateThrowEvent_03gco2y", 
                               "Task_1k2a6ug", "IntermediateThrowEvent_06uix62", "Task_1j6jppi", "IntermediateThrowEvent_0a4ziw0",
                               "Task_15lyv16", "IntermediateThrowEvent_02yuyn7", "Task_1lxvq1c", "IntermediateThrowEvent_1qv6g8u"]
    
    expected_result.message = "Flow Objects that are the source or target element of a " \
                               "Message Flow should have a Potential Evidence Source label."

    expected_output = Output()
    expected_output.warnings = [expected_result]

    assert len(output.warnings) == 1

    assert (sorted(expected_output.warnings[0].source) == sorted(output.warnings[0].source) and
            expected_output.warnings[0].message == output.warnings[0].message)

