from z3 import *
from zope.interface import implementer

from typing import List, Dict, Optional

from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.result import Result
from src.elements.flow_object.task.task import Task
from src.elements.frss.evidence_type.proof import HashProof
from src.elements.frss.forensic_ready_task.computations import IntegrityComputation

from src.rules.utils.evidence_quality import get_all_ev_data_stores
from src.rules.utils.semantic import create_z3_task_data_object
from src.rules.z3_types import mk_data_store, data_store_sort, stored_pe, pe_number, store_participant, \
                               object_name, object_id, object_type


@implementer(IRule)
class HashDiffEvidenceContext:
    """
    Rule: Hash Different Evidence Context
    Description: This rule checks if the Hash Proof is stored independently of Potential Evidence,
    i.e., in a different Evidence Context.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.message = "Hash Proof and Potential Evidence should be stored in a different Evidence Context."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        solutions = []

        # Create a list of all data stores present in the model
        z3_data_stores = get_all_ev_data_stores(elements, mk_data_store)

        for elem in elements.values():
            # Find all tasks that execute a hash function
            if not isinstance(elem, Task) or not isinstance(elem.computation, IntegrityComputation):
                continue
            
            # Create Z3 data objects from function input and output data object
            z3_fun_input = create_z3_task_data_object(elem, elem.computation.input, elements)
            z3_fun_output = create_z3_task_data_object(elem, elem.computation.output, elements)
            
            if str(simplify(object_type(z3_fun_output))).strip('"') != "HashProof":
                continue

            # Check if the data store exists in the model
            def data_store_exists(data_str):
                return Or([data_str == store for store in z3_data_stores])

            # Checks if there exists an index such that the array at that index contains the potential evidence
            def contains_evidence(index, data_str, data_obj):
                return Exists(index,
                                And(
                                    Select(stored_pe(data_str), index) == object_name(data_obj),
                                    # the array at the index contains the potential evidence name
                                    0 <= index,  # index is not negative
                                    index < pe_number(data_str)
                                    # index is not larger than the number of stored potential evidence
                                )
                            )

            # Set up the Z3 solver and add the constraints
            s = Solver()
            input_data_store = Const('input_data_store', data_store_sort)
            input_index = Int('input_index')

            output_data_store = Const('output_data_store', data_store_sort)
            output_index = Int('output_index')

            # Limit to data stores from the model
            s.add(data_store_exists(input_data_store))
            s.add(data_store_exists(output_data_store))

            # Check that the data stores contains input or output data object
            s.add(contains_evidence(input_index, input_data_store, z3_fun_input))
            s.add(contains_evidence(output_index, output_data_store, z3_fun_output))

            # Check that the evidence context is different
            s.add(store_participant(input_data_store) != store_participant(output_data_store))

            if s.check() == unsat:
                solutions.append(str(simplify(object_id(z3_fun_input))).strip('"'))
                solutions.append(str(simplify(object_id(z3_fun_output))).strip('"'))

        return self.__create_result(solutions) if len(solutions) > 0 else None
