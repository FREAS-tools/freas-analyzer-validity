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
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, object_name


@implementer(IRule)
class KeyedHashFunOutput:
    """
    Rule: Keyed Hash Function Output
    Description: This rule checks if Keyed Hash Function has exactly one output, being a Keyed Hash Proof.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        error = Error()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Task that executes the Keyed Hash Function must have exactly one output, " \
                        "Potential Evidence, being a Keyed Hash Proof."

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        s = Solver()
        solutions = []

        for elem_id, elem in elements.items():
            if not isinstance(elem, Task) or elem.hash_fun is None or \
                    elem.hash_fun.key is None or elem.pe_source is None:
                continue

            s.push()

            data_ref: str = elem.hash_fun.output
            ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
            data_obj: Optional[DataObject] = elements.get(ref_obj.data)

            assert data_obj is not None

            participant = get_participant(elements, data_obj.process_id)
            hash_output = mk_data_object(StringVal(participant), StringVal(elem_id), StringVal(data_obj.id),
                                         StringVal(ref_obj.name), StringVal(type(data_obj).__name__))

            # data needed to check that task contains only one output
            outputs = []  # contains all output data objects from the current task

            for output in elem.data_output:
                data_ref: str = output.target_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: Optional[DataObject] = elements.get(ref_obj.data)

                assert data_obj is not None
                
                participant = get_participant(elements, data_obj.process_id)
                outputs.append(mk_data_object(StringVal(participant), StringVal(elem_id),
                                              StringVal(data_obj.id), StringVal(ref_obj.name),
                                              StringVal(type(data_obj).__name__)))

            if len(outputs) == 0:
                outputs = create_mock_data_objects(0, 1, mk_data_object, elem_id)

            # Compare hash function output data object (Hash Proof) id with the provided data object
            # also checks that the output is the same object as output of the hash function
            # then we know that both task output assoc and pes output assoc point to the same object
            def single_output(data_object):
                return And(participant_id(hash_output) == participant_id(data_object),
                           task_id(hash_output) == task_id(data_object),
                           object_id(hash_output) == object_id(data_object),
                           object_name(hash_output) == object_name(data_object),
                           object_type(hash_output) == object_type(data_object))

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'KeyedHashProof'

            # Compare output object with the provided data object
            def exists(data_object):
                return Or([And(participant_id(o) == participant_id(data_object), task_id(o) == task_id(data_object), 
                               object_name(o) == object_name(data_object), object_id(o) == object_id(data_object),
                               object_type(o) == object_type(data_object))
                           for o in outputs])

            z3_data_object = Const('z3_data_object', data_object_sort)

            # Data object different from function output exists => multiple data outputs
            # or data object has different type then Hash Proof
            s.add(Or(Not(single_output(z3_data_object)), Not(correct_type(z3_data_object))))

            # Data object is contained in task output objects
            s.add(exists(z3_data_object))

            if s.check() == sat:
                model = s.model()
                solutions.append(str(simplify(task_id(model[z3_data_object]))).strip('"'))  # only element's ID

            s.pop()

        return self.__create_result(solutions) if len(solutions) > 0 else None
