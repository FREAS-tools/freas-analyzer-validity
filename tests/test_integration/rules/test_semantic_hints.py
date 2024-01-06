from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.analyzer.analyzer import Analyzer
from src.parser.parser import parse
from src.rules.rule_result.result import Result


# def test_semantic_hints(keyed_hash_reused_key):
#     analysis_type = AnalysisType.SEMANTIC_HINTS
#     analysis_input = Input(analysis_type, None)

#     output = Analyzer.analyze(analysis_input, keyed_hash_reused_key)

#     expected_warning_1 = Result()
#     expected_warning_1.source = ["Event_07viqfw"]
#     expected_warning_1.message = "Flow Objects that are the source or target element of a " \
#                                  "Message Flow should have a Potential Evidence Source label"

#     expected_warning_2 = Result()
#     expected_warning_2.source = ["Participant_04cmj4g", "Participant_150mijc"]
#     expected_warning_2.message = "The key used in Keyed Hash Function must not be used in different Pool."

#     expected_output = Output()
#     expected_output.warnings = [expected_warning_1, expected_warning_2]

#     assert len(output.warnings) == 2

#     assert (sorted(expected_output.warnings[0].source) == sorted(output.warnings[0].source) and
#             expected_output.warnings[0].message == output.warnings[0].message) or \
#            (sorted(expected_output.warnings[0].source) == sorted(output.warnings[1].source) and
#             expected_output.warnings[0].message == output.warnings[1].message)

#     assert (sorted(expected_output.warnings[1].source) == sorted(output.warnings[0].source) and
#             expected_output.warnings[1].message == output.warnings[0].message) or \
#            (sorted(expected_output.warnings[1].source) == sorted(output.warnings[1].source) and
#             expected_output.warnings[1].message == output.warnings[1].message)

