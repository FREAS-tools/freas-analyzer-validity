import os
import pytest

from src.parser.parser import Parser

"""
The following fixtures are used to test the implemented rules.
"""

# Path to Scenario diagrams directory
scenario_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../diagrams/scenarios/'))

# Path to Computation diagrams directory
computations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../diagrams/computation/'))

# Path to Evidence quality diagrams directory
evidence_quality_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../diagrams/evidence_quality/'))

# Path to Evidence oriented diagrams directory
evidence_oriented_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../diagrams/evidence_oriented/'))


# Fixtures for the testing scenarios

@pytest.fixture(scope="session")
def rics_issuing_permit():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "rics_issuing_permit.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def rics_issuing_permit_missing_pes():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "rics_issuing_permit_missing_pes.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def rics_issuing_permit_reservation_storage():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "rics_issuing_permit_reservation_storage.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def rics_issuing_permit_log_storage():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "rics_issuing_permit_log_storage.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def av_scenario():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "av_scenario.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def av_parking_register():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "av-parking_register.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def av_issuing_permit():
    parser = Parser()
    file_path = os.path.join(scenario_dir, "av_issuing_permit.bpmn")
    return parser.parse_file(file_path)


# Fixtures for the testing evidence and evidence source
@pytest.fixture(scope="session")
def semantics_bad_elements():
    parser = Parser()
    file_path = os.path.join(evidence_oriented_dir, "missing_potential_evidence.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def semantics_good_elements():
    parser = Parser()
    file_path = os.path.join(evidence_oriented_dir, "contains_potential_evidence.bpmn")
    return parser.parse_file(file_path)


# Fixtures for the testing evidence quality
@pytest.fixture(scope="session")
def disputable_same_store_elements():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "disputable_stored_in_same_store.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def disputable_same_context_elements():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "disputable_stored_in_same_context.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def disputable_stored_on_user_device():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "disputable_stored_on_user_device.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def evidence_quality():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "evidence_quality.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def different_evidence_context():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "different_evidence_context.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def before_after():
    parser = Parser()
    file_path = os.path.join(evidence_quality_dir, "before_after_diagram.bpmn")
    return parser.parse_file(file_path)


# Fixtures for the testing computations
@pytest.fixture(scope="session")
def all_computations_one_input_output():
    parser = Parser()
    file_path = os.path.join(computations_dir, "all_computations.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def all_computations_bad_io_type():
    parser = Parser()
    file_path = os.path.join(computations_dir, "all_computations_bad_io_type.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def all_computations_with_pes():
    parser = Parser()
    file_path = os.path.join(computations_dir, "all_computations_with_pes.bpmn")
    return parser.parse_file(file_path)


## Fixtures for the testing integrity computations
@pytest.fixture(scope="session")
def integrity_computation_one_input():
    parser = Parser()
    file_path = os.path.join(computations_dir, "integrity_computation_one_input.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def integrity_computation_two_inputs():
    parser = Parser()
    file_path = os.path.join(computations_dir, "integrity_computation_two_inputs.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def integrity_computation_three_inputs():
    parser = Parser()
    file_path = os.path.join(computations_dir, "integrity_computation_three_inputs.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def integrity_computation_output_good():
    parser = Parser()
    file_path = os.path.join(computations_dir, "integrity_computation_output_good.bpmn")
    return parser.parse_file(file_path)


## Fixtures for the testing keyed hash functions
@pytest.fixture(scope="session")
def keyed_hash_reused_key():
    parser = Parser()
    file_path = os.path.join(computations_dir, "keyed_hash_reused_key.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def keyed_hash_fun_input_output():
    parser = Parser()
    file_path = os.path.join(computations_dir, "keyed_hash_fun.bpmn")
    return parser.parse_file(file_path)


@pytest.fixture(scope="session")
def keyed_hash_fun_bad_input_output():
    parser = Parser()
    file_path = os.path.join(computations_dir, "keyed_hash_fun_bad_io.bpmn")
    return parser.parse_file(file_path)
