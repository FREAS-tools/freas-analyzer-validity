import os
import pytest

from src.parser.parser import parse

"""
The following fixtures are used to test the implemented rules.
"""

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documentation/diagrams/'))

@pytest.fixture
def new_av_scenario():
    file_path = os.path.join(data_dir, "new_av_scenario.bpmn")
    return parse(file_path)


@pytest.fixture
def missing_pes_elements():
    file_path = os.path.join(data_dir, "missing_evidence_source.bpmn")
    return parse(file_path)


@pytest.fixture
def semantics_bad_elements():
    file_path = os.path.join(data_dir, "missing_potential_evidence.bpmn")
    return parse(file_path)


@pytest.fixture
def semantics_good_elements():
    file_path = os.path.join(data_dir, "semantics_good.bpmn")
    return parse(file_path)


@pytest.fixture
def hash_correct_elements():
    file_path = os.path.join(data_dir, "hash_correct.bpmn")
    return parse(file_path)


@pytest.fixture
def keyed_hash_correct_elements():
    file_path = os.path.join(data_dir, "keyed_hash_correct.bpmn")
    return parse(file_path)


@pytest.fixture
def keyed_hash_reused_elements():
    file_path = os.path.join(data_dir, "keyed_hash_reused.bpmn")
    return parse(file_path)


@pytest.fixture
def keyed_hash_unique_elements():
    file_path = os.path.join(data_dir, "keyed_hash_unique.bpmn")
    return parse(file_path)


@pytest.fixture
def disputable_same_store_elements():
    file_path = os.path.join(data_dir, "disputable_stored_in_same_store.bpmn")
    return parse(file_path)


@pytest.fixture
def disputable_same_context_elements():
    file_path = os.path.join(data_dir, "disputable_stored_in_same_context.bpmn")
    return parse(file_path)


@pytest.fixture
def hash_missing_pes_elements():
    file_path = os.path.join(data_dir, "hash_missing_pes.bpmn")
    return parse(file_path)


@pytest.fixture
def hash_correct_pes_elements():
    file_path = os.path.join(data_dir, "keyed_hash_unique.bpmn")
    return parse(file_path)