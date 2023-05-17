import pytest

from parser.parser import parse

"""
The following fixtures are used to test the implemented rules.
"""


@pytest.fixture
def missing_pes_elements():
    return parse("../../../documentation/diagrams/missing_evidence_source.bpmn")


@pytest.fixture
def semantics_bad_elements():
    return parse("../../../documentation/diagrams/missing_potential_evidence.bpmn")


@pytest.fixture
def semantics_good_elements():
    return parse("../../../documentation/diagrams/semantics_good.bpmn")


@pytest.fixture
def hash_correct_elements():
    return parse("../../../documentation/diagrams/hash_correct.bpmn")


@pytest.fixture
def keyed_hash_correct_elements():
    return parse("../../../documentation/diagrams/keyed_hash_correct.bpmn")


@pytest.fixture
def keyed_hash_reused_elements():
    return parse("../../../documentation/diagrams/keyed_hash_reused.bpmn")


@pytest.fixture
def keyed_hash_unique_elements():
    return parse("../../../documentation/diagrams/keyed_hash_unique.bpmn")


@pytest.fixture
def disputable_same_store_elements():
    return parse("../../../documentation/diagrams/disputable_stored_in_same_store.bpmn")


@pytest.fixture
def disputable_same_context_elements():
    return parse("../../../documentation/diagrams/disputable_stored_in_same_context.bpmn")


@pytest.fixture
def hash_missing_pes_elements():
    return parse("../../../documentation/diagrams/hash_missing_pes.bpmn")


@pytest.fixture
def hash_correct_pes_elements():
    return parse("../../../documentation/diagrams/keyed_hash_unique.bpmn")
