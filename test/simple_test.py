from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.response.response import Response
from src.parser.parser import parse

import os


def test_compromised_data_store_pe():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../documentation/diagrams/new_av_scenario.bpmn'))

    elements = parse(file_path)
    rule = CompromisedDataStore()
    result = rule.evaluate(elements, "DataStoreReference_0a5zo83")
    expected_result = Response()
    expected_result.source = ["DataStore_0kxtat1"]

    assert isinstance(result, Response)
    assert sorted(result.source) == sorted(expected_result.source)
