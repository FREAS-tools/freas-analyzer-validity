from z3 import StringVal

from typing import Dict

from src.elements.element import Element
from src.elements.container.pool import Pool


def create_mock_data_objects(current, expected, constructor, task_id):
    """
    Create mock data objects based on the given parameters.

    Parameters:
        current (int): The current number of data objects value.
        expected (int): The expected number of data objects value.
        constructor (function): The constructor function to create the mock data objects.
        task_id (str): The task ID.

    Returns:
        list: A list of mock data objects.
    """
    mock_inputs = []
    while current != expected:
        mock_inputs.append(constructor(StringVal("MockParticipant"), StringVal(task_id), StringVal(f"MockID{current}"),
                                       StringVal(f"MockName{current}"), StringVal("MockType")))
        current += 1

    return mock_inputs


def get_participant(elements: Dict[str, Element], process_id) -> str:
    """
    Get the participant ID associated with the given process ID.

    Parameters:
        elements (Dict[str, Element]): A dictionary of elements.
        process_id: The process ID to search for.

    Returns:
        str: The participant ID if found, otherwise an empty string.
    """
    for elem in elements.values():
        if isinstance(elem, Pool) and elem.process_ref == process_id:
            return elem.id

    return ""
