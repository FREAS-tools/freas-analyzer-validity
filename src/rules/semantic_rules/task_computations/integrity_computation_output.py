from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.result import Result
from src.elements.flow_object.task.task import Task
from src.rules.rule_result.severity import Severity
from src.elements.artefact.data_store.data_store import DataStore
from src.elements.artefact.data_object.data_object import DataObject
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.frss.forensic_ready_task.computations import IntegrityComputation

from src.rules.utils.semantic import create_mock_data_objects, get_participant, get_task_output_object
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, object_name


@implementer(IRule)
class IntegrityComputationOutput:
    """
    Rule: Integrity Computation Output
    Description: This rule checks if Integrity Computation has exactly one output, being a Potential Evidence or a Hash Proof.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.severity = Severity.MEDIUM
        result.message = "Task that executes the Integrity Computation must have exactly one output, " \
                        "being a Potential Evidence or a Hash Proof."
        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        s = Solver()
        solutions = []

        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.computation is None or not isinstance(elem.computation, IntegrityComputation):
                continue
            
            s.push()

            data_obj = get_task_output_object(elem, elem.computation.output, elements)
            participant = get_participant(elements, data_obj.process_id)

            z3_comp_output = mk_data_object(StringVal(participant), StringVal(key), StringVal(data_obj.id),
                                         StringVal(data_obj.name), StringVal(type(data_obj).__name__))

            z3_task_outputs = []

            for output in elem.data_output:
                data_ref: str = output.target_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj = elements.get(ref_obj.data)

                if isinstance(data_obj, DataStore):
                    continue
                
                assert data_obj is not None
                
                participant = get_participant(elements, data_obj.process_id)
                z3_task_outputs.append(mk_data_object(StringVal(participant), StringVal(key), StringVal(data_obj.id),
                                                      StringVal(ref_obj.name), StringVal(type(data_obj).__name__)))

            if len(z3_task_outputs) == 0:
                z3_task_outputs = create_mock_data_objects(0, 1, mk_data_object, key)

            def single_output(data_object):
                return data_object == z3_comp_output

            def correct_type(data_object):
                return Or(simplify(object_type(data_object)) == 'PotentialEvidenceType', simplify(object_type(data_object)) == 'HashProof')

            # Compare output objects with the provided data object
            def exists(data_object):
                return Or([data_object == obj for obj in z3_task_outputs])

            z3_data_object = Const('data_object', data_object_sort)

            # Data object different from function output exists => multiple data outputs
            # or data object has different type then Hash Proof
            s.add(Or(Not(single_output(z3_data_object)), Not(correct_type(z3_data_object))))
            # s.add(Not(single_output(x)))

            # data object is contained in task output objects
            s.add(exists(z3_data_object))

            # no need for while loop since we need the task not particular data objects
            if s.check() == sat:
                model = s.model()
                solutions.append(str(simplify(task_id(model[z3_data_object]))).strip('"'))  # only element's ID

            s.pop()

        return self.__create_result(solutions) if len(solutions) > 0 else None
