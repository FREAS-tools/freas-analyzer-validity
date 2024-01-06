from z3 import *
from zope.interface import implementer

from typing import List, Dict, Optional

from src.elements.artefact.data_object.data_object import DataObject
from src.elements.element import Element
from src.elements.flow_object.task.task import Task
from src.rules.rule_result.result import Result
from src.rules.rule import IRule
from src.elements.artefact.data_reference import DataObjectReference

from src.rules.utils.semantic import get_participant
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_type, object_name

@implementer(IRule)
class SameEvidenceStore:
    """
    Rule: Same Evidence Store
    Description: This rule checks if the Hash Proof is stored independently of Potential Evidence,
    i.e., in a different Evidence Context.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.message = "The HashProof must be stored independently of Potential Evidence," \
                          " i.e., in a different Evidence Context."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        solutions = []

        for elem in elements.values():
            # Find all tasks that execute a hash function
            if not isinstance(elem, Task) or elem.hash_fun is None:
                continue

            # Find the input and output data objects of the hash function
            # and create a Z3 DataObject representing them
            input_ref: DataObjectReference = elements[elem.hash_fun.input]
            fun_input: DataObject = elements[input_ref.data]
            participant = get_participant(elements, fun_input.process_id)
            
            # Task id is not relevant, thus the "None" value
            z3_fun_input = mk_data_object(StringVal(participant), StringVal("None"), StringVal(fun_input.id), 
                                          StringVal(input_ref.name), StringVal(type(fun_input).__name__))

            output_ref = elements[elem.hash_fun.output]
            fun_output = elements[output_ref.data]
            participant = get_participant(elements, fun_output.process_id)

            z3_fun_output = mk_data_object(StringVal(participant), StringVal("None"), StringVal(fun_output.id), 
                                           StringVal(output_ref.name), StringVal(type(fun_output).__name__))

            # Get all data objects in the model and create Z3 DataObject representing them
            z3_data_objects = []
            for value in elements.values():
                if not isinstance(value, DataObject):
                    continue

                participant = get_participant(elements, value.process_id)
                z3_data_objects.append(mk_data_object(StringVal(participant), StringVal("None"), StringVal(value.id), StringVal(value.name), StringVal(type(value).__name__)))

            def exists(data_object):
                return Or([data_object == obj for obj in z3_data_objects])

            def stored(data_object):
                return And(
                    [Or(participant_id(data_object) == participant_id(obj), object_name(data_object) != object_name(obj))
                     for obj in z3_data_objects]
                )
            
            s = Solver()
            proof = Const('proof', data_object_sort)
            pot_evidence = Const('pot_evidence', data_object_sort)

            s.add(And(exists(proof), exists(pot_evidence)))

            s.add(pot_evidence == z3_fun_input)
            s.add(proof == z3_fun_output)
            
            s.add(stored(proof))
            s.add(stored(pot_evidence))

            while s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    s.add(dec() != model[dec])
                    solutions.append(str(simplify(object_id(model[dec]))).strip('"'))  # only element's ID

        return self.__create_result(solutions) if len(solutions) > 0 else None
