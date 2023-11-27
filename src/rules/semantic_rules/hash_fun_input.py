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
                return data_object == z3_hash_input

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def exists(data_object):
                return Or([data_object == obj for obj in inputs])

            z3_data_object = Const('data_object', data_object_sort)

            # Data object different from function output exists => multiple data inputs
            # or data object has different type then PotentialEvidenceType
            s.add(Or(Not(single_input(z3_data_object)), Not(correct_type(z3_data_object))))

            # Data object is contained in task output objects
            s.add(exists(z3_data_object))

            if s.check() == sat:
                model = s.model()
                solutions.append(str(simplify(task_id(model[z3_data_object]))).strip('"'))  # only element's ID

            s.pop()

        return self.__create_result(solutions) if len(solutions) > 0 else None
