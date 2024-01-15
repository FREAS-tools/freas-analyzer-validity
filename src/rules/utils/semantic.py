from z3 import StringVal

from typing import Dict, Optional

from src.elements.element import Element
from src.elements.container.pool import Pool
from src.elements.flow_object.task.task import Task
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.artefact.data_object.data_object import DataObject

from src.rules.z3_types import mk_data_object


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
        elements (Dict[str, Element]): A dictionary of model elements.
        process_id: The process ID to search for.

    Returns:
        str: The participant ID if found, otherwise an empty string.
    """
    for elem in elements.values():
        if isinstance(elem, Pool) and elem.process_ref == process_id:
            return elem.id

    return ""


def get_task_input_object(task: Task, input_association: str, elements: Dict[str, Element]) -> Optional[DataObject]:
    """
    Get the data object associated with the given task and input association.

    Parameters:
        task (Task): The task being checked.
        input_association (str): The input association from the data object to the task.
        elements (Dict[str, Element]): A dictionary of model elements.

    Returns:
        DataObject: The data object if found, otherwise None.
    """
    
    for input_ in task.data_input:
        if input_.id == input_association:
            ref_obj: Optional[DataObjectReference] = elements.get(input_.source_ref)
            data_object = elements.get(ref_obj.data)
            data_object.name = ref_obj.name

            return data_object

    return None


def get_task_output_object(task: Task, output_association: str, elements: Dict[str, Element]) -> Optional[DataObject]:
    """
    Get the data object associated with the given task and output association.

    Parameters:
        task (Task): The task being checked.
        output_association (str): The output association from the task to the data object.
        elements (Dict[str, Element]): A dictionary of model elements.

    Returns:
        DataObject: The data object if found, otherwise None.
    """
    for output in task.data_output:
        if output.id == output_association:
            ref_obj: Optional[DataObjectReference] = elements.get(output.target_ref)
            data_object = elements.get(ref_obj.data)
            data_object.name = ref_obj.name

            return data_object

    return None


def create_z3_data_object(task: Task, data_object_id: str, elements: Dict[str, Element], input=True):
    """
    Create a Z3 data object based on the given parameters.

    Parameters:
        task (Task): The task containing the data object.
        data_object_id (str): The data object ID.
        elements (Dict[str, Element]): A dictionary of model elements.
        input (bool): Whether the data object is an input or output.

    Returns:
        Z3 DataObject: Z3 data object if found, otherwise None.
    """
    data_objects = task.data_input if input else task.data_output

    for obj in data_objects:
        if obj.id == data_object_id:
            ref_id: str = obj.source_ref if input else obj.target_ref
            ref_obj: DataObjectReference = elements[ref_id]
            data_object: DataObject = elements[ref_obj.data]
            participant = get_participant(elements, data_object.process_id)
    
            return mk_data_object(StringVal(participant), StringVal(task.id), StringVal(data_object.id), 
                                  StringVal(ref_obj.name), StringVal(type(data_object).__name__))

    return None