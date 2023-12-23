from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.error import Error
from src.rules.rule_result.result import Result
from src.elements.flow_object.task.task import Task
from src.rules.rule_result.severity import Severity
from src.elements.artefact.data_object.data_object import DataObject
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.frss.forensic_ready_task.computations import HashFunction

from src.rules.utils.semantic import create_mock_data_objects, get_participant
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, \
    object_name


@implementer(IRule)
class KeyedHashFunInput:
    """
    Rule: Keyed Hash Function Input
    Description: This rule checks if Keyed Hash Function receives a Potential Evidence Type and a key as an input.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        error = Error()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Task that executes the Keyed Hash Function must have exactly two inputs, " \
                        "one being a Potential Evidence Type, and a key."
        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        s = Solver()
        solutions = []

        for elem_id, elem in elements.items():
            # Check if element is a task performing keyed hash function
            if not isinstance(elem, Task) or elem.computation is None or \
               not isinstance(elem.computation, HashFunction) or elem.computation.key is None:
                continue

            s.push()

            z3_task_inputs = []
            for input_ in elem.data_input:
                data_ref_id = input_.source_ref
                data_ref: DataObjectReference = elements[data_ref_id]
                data_obj: DataObject = elements[data_ref.data]

                assert data_obj is not None

                participant = get_participant(elements, data_obj.process_id)
                z3_task_inputs.append(mk_data_object(StringVal(participant), StringVal(elem_id), StringVal(data_obj.id),
                                                     StringVal(data_ref.name), StringVal(type(data_obj).__name__)))

            if len(z3_task_inputs) < 2:
                z3_task_inputs += create_mock_data_objects(len(z3_task_inputs), 2, mk_data_object, elem_id)

            def two_inputs():
                return len(z3_task_inputs) == 2

            def correct_data_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def correct_key_type(data_object):
                return simplify(object_name(data_object)) == 'key'

            def equal(data_object, key_object):
                return data_object == key_object

            def exists(data_object):
                return Or([data_object == obj for obj in z3_task_inputs])

            input_one = Const('input_one', data_object_sort)
            input_two = Const('input_two', data_object_sort)

            correct_types = Or(And(correct_data_type(input_one), correct_key_type(input_two)),
                               And(correct_data_type(input_two), correct_key_type(input_one)))

            s.add(Or(Not(two_inputs()), Not(correct_types)))
            s.add(And(exists(input_one), exists(input_two)))
            s.add(Not(equal(input_one, input_two)))

            if s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    s.add(dec() != model[dec])  # no duplicates
                    solutions.append(str(simplify(task_id(model[dec]))).strip('"'))  # only element's ID
                    break

            s.pop()

        return self.__create_result(solutions) if len(solutions) > 0 else None
