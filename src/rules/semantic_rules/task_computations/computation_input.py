from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.result import Result
from src.elements.flow_object.task.task import Task
from src.rules.rule_result.severity import Severity
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.artefact.data_object.data_object import DataObject
from src.elements.frss.forensic_ready_task.computations import HashFunction

from src.rules.utils.semantic import create_mock_data_objects, get_participant, get_task_input_object
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, \
    object_name


@implementer(IRule)
class ComputationInput:
    """
    Rule: Computation Input
    Description: This rule checks if a task performing any type of computation, 
    except Keyed hash function, receives a Potential Evidence Type as the only input.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.severity = Severity.MEDIUM
        result.message = "Task performing a computation must have exactly one input, " \
                          "being a Potential Evidence Type."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        s = Solver()
        solutions = []

        # Goes through all task and checks their if they are a computation task, disregarding keyed hash functions
        # as it has multiple inputs (key and data)
        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.computation is None or \
                (isinstance(elem.computation, HashFunction) and elem.computation.key is not None):
                continue
            
            s.push()

            # Get the data object associated with the task input
            data_obj = get_task_input_object(elem, elem.computation.input, elements)
            participant = get_participant(elements, data_obj.process_id)
            
            z3_input = mk_data_object(StringVal(participant), StringVal(key),
                                      StringVal(data_obj.id), StringVal(data_obj.name),
                                      StringVal(type(data_obj).__name__))
            
            z3_task_inputs = []

            for input_ in elem.data_input:
                data_ref: str = input_.source_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: Optional[DataObject] = elements.get(ref_obj.data)

                assert data_obj is not None

                z3_task_inputs.append(mk_data_object(StringVal(participant), StringVal(key),
                                             StringVal(data_obj.id), StringVal(ref_obj.name),
                                             StringVal(type(data_obj).__name__)))

            if len(z3_task_inputs) == 0:
                z3_task_inputs = create_mock_data_objects(0, 1, mk_data_object, key)

            def single_input(data_object):
                return data_object == z3_input

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def exists(data_object):
                return Or([data_object == obj for obj in z3_task_inputs])

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
