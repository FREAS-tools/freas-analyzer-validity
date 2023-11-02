# from analyzer.analyzer import Analyzer
# from input.analysis_types import AnalysisType
# from input.input import Input
# from parser.parser import parse
# from response.response import Response
# from result.result import Result


# def test_quality_evidence_analysis():
#     file_path = "../../../data/diagrams/disputable_stored_in_same_store.bpmn"
#     analysis_type = AnalysisType.EVIDENCE_QUALITY_ANALYSIS
#     element_id = "Activity_19xl907"

#     try:
#         analysis_input = Input(analysis_type, element_id)
#         bpmn4frss_elements = parse(file_path)
#     except Exception as e:
#         print("Error while parsing the BPMN4FRSS model: " + str(e))
#         return

#     result = Analyzer.analyze(analysis_input, bpmn4frss_elements)

#     expected_response = Response()
#     expected_response.source = ["DataStore_1qqlqq2"]

#     expected_result = Result()
#     expected_result.evidence_sources = expected_response

#     assert isinstance(result, Result)

#     assert sorted(result.evidence_sources.source) == sorted(expected_result.evidence_sources.source)

