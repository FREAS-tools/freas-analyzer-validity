import os
import pytest

from src.parser.parser import Parser

"""
The following fixtures are used to test the implemented rules.
"""

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/diagrams/'))

@pytest.fixture(scope="session")
def new_av_scenario():
    parser = Parser()
    file_path = os.path.join(data_dir, "new_av_scenario.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def missing_pes_elements():
    parser = Parser()
    file_path = os.path.join(data_dir, "missing_evidence_source.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def semantics_bad_elements():
    parser = Parser()
    file_path = os.path.join(data_dir, "missing_potential_evidence.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def semantics_good_elements():
    parser = Parser()
    file_path = os.path.join(data_dir, "contains_potential_evidence.bpmn")
    return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def hash_correct_elements():
#     file_path = os.path.join(data_dir, "hash_correct.bpmn")
#     return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def keyed_hash_correct_elements():
#     file_path = os.path.join(data_dir, "keyed_hash_correct.bpmn")
#     return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def keyed_hash_reused_elements():
#     file_path = os.path.join(data_dir, "keyed_hash_reused.bpmn")
#     return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def keyed_hash_unique_elements():
#     file_path = os.path.join(data_dir, "keyed_hash_unique.bpmn")
#     return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def disputable_same_store_elements():
    parser = Parser()
    file_path = os.path.join(data_dir, "disputable_stored_in_same_store.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def disputable_same_context_elements():
    parser = Parser()
    file_path = os.path.join(data_dir, "disputable_stored_in_same_context.bpmn")
    return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def hash_missing_pes_elements():
#     parser = Parser()
#     file_path = os.path.join(data_dir, "hash_missing_pes.bpmn")
#     return parser.parse_file(file_path)


# @pytest.fixture(scope="session")
# def hash_correct_pes_elements():
#     file_path = os.path.join(data_dir, "keyed_hash_unique.bpmn")
#     return parser.parse_file(file_path)
