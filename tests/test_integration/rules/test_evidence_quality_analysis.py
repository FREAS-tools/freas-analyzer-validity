from src.analysis_output.output import Output
from src.rules.rule_result.result import Result
from src.analysis_input.input import Input
from src.analysis_input.analysis_types import AnalysisType
from src.analyzer.analyzer import Analyzer
from src.parser.parser import parse


def test_evidence_quality_analysis(disputable_same_store_elements):
    analysis_type = AnalysisType.EVIDENCE_QUALITY_ANALYSIS
    element_id = "Task_0pcmu9v"
    
    analysis_input = Input(analysis_type, element_id)

    output = Analyzer.analyze(analysis_input, disputable_same_store_elements)

    expected_result = Result()
    expected_result.source = ["DataStore_0zf3t9g"]

    assert sorted(output.evidence_sources.source) == sorted(expected_result.source)

