from z3 import StringVal


def add_mock_inputs(task_id, count, constructor):
    mock_inputs = [constructor(StringVal(task_id), StringVal("None_1"),
                               StringVal("None_1"), StringVal("MockDataObject"))]
    if count == 1:
        return mock_inputs

    mock_inputs.append(constructor(StringVal(task_id), StringVal("None_2"),
                                   StringVal("None_2"), StringVal("MockDataObject")))
    return mock_inputs
