# from analyzer.analyzer import Analyzer
# from input.analysis_types import AnalysisType
# from input.input import Input
# from parser.parser import parse
# from response.warning import Warning
# from result.result import Result


# def test_quality_evidence_analysis():
#     file_path = "../../../data/diagrams/av-parking_register.bpmn"
#     analysis_type = AnalysisType.SEMANTIC_ALL

#     try:
#         analysis_input = Input(analysis_type, None)
#         bpmn4frss_elements = parse(file_path)
#     except Exception as e:
#         print("Error while parsing the BPMN4FRSS model: " + str(e))
#         return

#     result = Analyzer.analyze(analysis_input, bpmn4frss_elements)

#     expected_warning = Warning()
#     expected_warning.source = ["Activity_0vqb0h1", "Event_1kwr4k9", "Activity_04iyke1", "Event_0e8vxiy"]
#     expected_warning.message = "Flow Objects that are the source or target element of a " \
#                                "Message Flow should have a Potential Evidence Source label"

#     expected_result = Result()
#     expected_result.warnings = [expected_warning]

#     assert isinstance(result, Result)
#     assert len(result.warnings) == 1

#     assert (sorted(expected_result.warnings[0].source) == sorted(result.warnings[0].source) and
#             expected_result.warnings[0].message == result.warnings[0].message)
