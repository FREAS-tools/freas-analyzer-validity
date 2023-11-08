from typing import List, Dict, Optional

from z3 import *
from zope.interface import implementer

from src.elements.artefact.data_object.data_object import DataObject
from src.elements.element import Element
from src.elements.flow_object.task.task import Task
from src.response.response import Response
from src.response.warning import Warning
from src.rules.rule import IRule
from src.rules.utils.semantic import get_participant


@implementer(IRule)
class SameEvidenceStore:
    """
    Rule: Same Evidence Store
    Description: This rule checks if the Hash Proof is stored independently of Potential Evidence,
    i.e., in a different Evidence Context.
    """

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        warning = Warning()
        warning.source = solutions
        warning.message = "The HashProof must be stored independently of Potential Evidence," \
                          " i.e., in a different Evidence Context."

        return warning

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:

        # Define the Z3 tuple sort representing data object, containing the following fields:
        # participant ID, data object id, and data object name
        data_object_sort, mk_data_object, (participant_id, object_id, object_name) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort()])

        solutions = []
        for key, elem in elements.items():
            # Find all tasks that execute a hash function
            if not isinstance(elem, Task) or elem.hash_fun is None:
                continue

            # Find the input and output data objects of the hash function
            # and create a Z3 DataObject representing them
            input_ref = elements[elem.hash_fun.input]
            fun_input = elements[input_ref.data]
            participant = get_participant(elements, fun_input.process_id)

            z3_fun_input = mk_data_object(StringVal(participant), StringVal(fun_input.id), StringVal(input_ref.name))

            output_ref = elements[elem.hash_fun.output]
            fun_output = elements[output_ref.data]
            participant = get_participant(elements, fun_output.process_id)

            z3_fun_output = mk_data_object(StringVal(participant), StringVal(fun_output.id), StringVal(output_ref.name))

            # Get all data objects in the model and create Z3 DataObject representing them
            z3_data_objects = []
            for value in elements.values():
                if not isinstance(value, DataObject):
                    continue

                participant = get_participant(elements, value.process_id)
                z3_data_objects.append(mk_data_object(StringVal(participant), StringVal(value.id), StringVal(value.name)))

            def exists(data_object):
                return Or([data_object == obj for obj in z3_data_objects])

            s = Solver()
            proof = Const('proof', data_object_sort)
            pot_evidence = Const('pot_evidence', data_object_sort)

            s.add(And(exists(proof), exists(pot_evidence)))

            def stored(obj):
                return And(
                    [Or(participant_id(obj) == participant_id(k), object_name(obj) != object_name(k))
                     for k in z3_data_objects]
                )

            s.add(proof == z3_fun_output)
            s.add(pot_evidence == z3_fun_input)
            s.add(stored(proof))
            s.add(stored(pot_evidence))

            while s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    s.add(dec() != model[dec])
                    solutions.append(str(simplify(object_id(model[dec]))).strip('"'))  # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None
