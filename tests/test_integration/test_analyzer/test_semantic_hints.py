# from analyzer.analyzer import Analyzer
# from input.analysis_types import AnalysisType
# from input.input import Input
# from parser.parser import parse
# from response.warning import Warning
# from result.result import Result


# def test_quality_evidence_analysis():
#     file_path = "../../../data/diagrams/keyed_hash_reused.bpmn"
#     analysis_type = AnalysisType.SEMANTIC_HINTS

#     try:
#         analysis_input = Input(analysis_type, None)
#         bpmn4frss_elements = parse(file_path)
#     except Exception as e:
#         print("Error while parsing the BPMN4FRSS model: " + str(e))
#         return

#     result = Analyzer.analyze(analysis_input, bpmn4frss_elements)

#     expected_warning_1 = Warning()
#     expected_warning_1.source = ["Event_07viqfw"]
#     expected_warning_1.message = "Flow Objects that are the source or target element of a " \
#                                  "Message Flow should have a Potential Evidence Source label"

#     expected_warning_2 = Warning()
#     expected_warning_2.source = ["Participant_04cmj4g", "Participant_150mijc"]
#     expected_warning_2.message = "The key used in Keyed Hash Function must not be used in different Pool."

#     expected_result = Result()
#     expected_result.warnings = [expected_warning_1, expected_warning_2]

#     assert isinstance(result, Result)
#     assert len(result.warnings) == 2

#     assert (sorted(expected_result.warnings[0].source) == sorted(result.warnings[0].source) and
#             expected_result.warnings[0].message == result.warnings[0].message) or \
#            (sorted(expected_result.warnings[0].source) == sorted(result.warnings[1].source) and
#             expected_result.warnings[0].message == result.warnings[1].message)

#     assert (sorted(expected_result.warnings[1].source) == sorted(result.warnings[0].source) and
#             expected_result.warnings[1].message == result.warnings[0].message) or \
#            (sorted(expected_result.warnings[1].source) == sorted(result.warnings[1].source) and
#             expected_result.warnings[1].message == result.warnings[1].message)
