from analyzer.analyzer import Analyzer
from input.analysis_types import AnalysisType
from input.input import Input
from parser.parser import parse
from response.error import Error
from result.result import Result


def test_quality_evidence_analysis():
    file_path = "../../../documentation/diagrams/hash_missing_pes.bpmn"
    analysis_type = AnalysisType.SEMANTIC_RULES

    try:
        analysis_input = Input(analysis_type, None)
        bpmn4frss_elements = parse(file_path)
    except Exception as e:
        print("Error while parsing the BPMN4FRSS model: " + str(e))
        return

    result = Analyzer.analyze(analysis_input, bpmn4frss_elements)

    expected_error = Error()
    expected_error.source = ["Activity_0l2nqgv"]
    expected_error.message = "Tasks that execute (Keyed) Hash function must have Potential Evidence Source label"

    expected_result = Result()
    expected_result.errors = [expected_error]

    assert isinstance(result, Result)
    assert len(result.errors) == 1

    assert (sorted(expected_result.errors[0].source) == sorted(result.errors[0].source) and
            expected_result.errors[0].message == result.errors[0].message)
