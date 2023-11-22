from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.elements.artefact.data_object.data_object import DataObject
from src.rules.rule import IRule
from src.rules.rule_result.error import Error
from src.elements.element import Element
from src.rules.rule_result.severity import Severity
from src.elements.flow_object.task.task import Task
from src.elements.artefact.data_reference import DataObjectReference
from src.rules.rule_result.result import Result

from src.rules.utils.semantic import create_mock_data_objects, get_participant
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, \
    object_name


@implementer(IRule)
class HashFunctionInput:
    """
    Rule: Hash Function Input
    Description: This rule checks if Hash Function receives a Potential Evidence Type as an input.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        error = Error()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Task that executes the Hash Function must have exactly one input, " \
                        "being a Potential Evidence Type."

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        s = Solver()
        solutions = []

        # Goes through all task and checks their output data objects
        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.hash_fun is None or elem.hash_fun.key is not None:
                continue

            s.push()

            data_ref: str = elem.hash_fun.input
            ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
            data_obj: Optional[DataObject] = elements.get(ref_obj.data)

            assert data_obj is not None

            participant = get_participant(elements, data_obj.process_id)
            z3_hash_input = mk_data_object(StringVal(participant), StringVal(key),
                                           StringVal(data_obj.id), StringVal(ref_obj.name),
                                           StringVal(type(data_obj).__name__))
            # Data needed to check that task contains only one input
            inputs = []

            for input_ in elem.data_input:
                data_ref: str = input_.source_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: Optional[DataObject] = elements.get(ref_obj.data)

                assert data_obj is not None

                inputs.append(mk_data_object(StringVal(participant), StringVal(key),
                                             StringVal(data_obj.id), StringVal(ref_obj.name),
                                             StringVal(type(data_obj).__name__)))

            if len(inputs) == 0:
                inputs = create_mock_data_objects(0, 1, mk_data_object, key)

            def single_input(data_object):
                return And(participant_id(z3_hash_input) == participant_id(data_object),
                           task_id(z3_hash_input) == task_id(data_object),
                           object_id(z3_hash_input) == object_id(data_object),
                           object_name(z3_hash_input) == object_name(data_object),
                           object_type(z3_hash_input) == object_type(data_object))

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def exists(data_object):
                return Or([And(participant_id(o) == participant_id(data_object), task_id(o) == task_id(data_object), 
                               object_name(o) == object_name(data_object), object_id(o) == object_id(data_object),
                               object_type(o) == object_type(data_object))
                           for o in inputs])

            x = Const('x', data_object_sort)

            # Data object different from function output exists => multiple data inputs
            # or data object has different type then PotentialEvidenceType
            s.add(Or(Not(single_input(x)), Not(correct_type(x))))

            # Data object is contained in task output objects
            s.add(exists(x))

            if s.check() == sat:
                model = s.model()
                solutions.append(str(simplify(task_id(model[x]))).strip('"'))  # only element's ID

            s.pop()

        return self.__create_result(solutions) if len(solutions) > 0 else None
