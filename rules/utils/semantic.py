from typing import Dict

from z3 import StringVal

from elements.element import Element
from elements.container.pool import Pool

"""
This file contains common functionality used by multiple rules when performing semantic analysis.
"""


def add_mock_inputs(task_id, count, constructor): # add cur and wanted num
    mock_inputs = [constructor(StringVal(task_id), StringVal("None_1"),
                               StringVal("None_1"), StringVal("MockDataObject"))]
    if count == 1:
        return mock_inputs

    mock_inputs.append(constructor(StringVal(task_id), StringVal("None_2"),
                                   StringVal("None_2"), StringVal("MockDataObject")))
    return mock_inputs


# def add_mock_outputs(task_id, count, constructor):


def get_participant(elements: Dict[str, Element], process_id) -> str:
    for elem in elements.values():
        if isinstance(elem, Pool) and elem.process_ref == process_id:
            return elem.id

    return ""
