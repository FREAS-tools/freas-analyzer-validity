from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.rules.rule_result.result import Result
from src.rules.rule import IRule
from src.elements.frss.evidence_data_store import EvidenceDataStore
from src.elements.element import Element
from src.elements.artefact.data_reference import DataStoreReference

from src.rules.z3_types import data_store_sort, mk_data_store, store_id, stored_pe, pe_number
from src.rules.utils.evidence_quality import get_potential_evidence, get_all_ev_data_stores, get_max_number_of_pe


@implementer(IRule)
class CompromisedDataStore:
    """
    Rule: Compromised Data Store
    Description: This rule checks availability of Data Stores that contain potential evidence
    relevant in case the marked Data Store is compromised.
    """

    @staticmethod
    def __create_result(solutions: List[str], data_store: str) -> Result:
        result = Result()
        result.source = solutions

        result.message = "Returned Data Stores contain potential evidence relevant in " \
                           "case that " + data_store + " is compromised."

        return result

    def evaluate(self, elements: Dict[str, Element], data_store_ref: str) -> Optional[Result]:

        data_store_ref_obj: Optional[DataStoreReference] = elements.get(data_store_ref)
        if data_store_ref_obj is None:
            return self.__create_result([], data_store_ref)

        data_store_id: str = data_store_ref_obj.data
        data_store = elements[data_store_id]

        if not isinstance(data_store, EvidenceDataStore):
            return self.__create_result([], data_store_ref)
        
        # Get a list of potential evidence that could indicate data store compromise
        z3_data_objects = get_potential_evidence(elements, data_store)
        
        # Return the maximum number of potential evidence that is stored in a data store
        max_pe_number = get_max_number_of_pe(elements)

        # Create a list of all data stores present in the model
        z3_data_stores = get_all_ev_data_stores(elements, mk_data_store)

        # Check if the data store exists in the model
        def exists(data_str):
            return Or(
                [And(store_id(data_str) == store_id(store), stored_pe(data_str) == stored_pe(store),
                     pe_number(data_str) == pe_number(store)) for store in z3_data_stores]
            )

        # Check if at least one potential evidence is stored in the data store
        def contains_relevant_evidence(data_str):
            constraint = []
            for data_obj in z3_data_objects:
                constraint.append(Or([And(Select(stored_pe(data_str), i) == data_obj, i < pe_number(data_str))
                                      for i in range(max_pe_number)]))

            return Or(constraint)

        # Set up the Z3 solver and add the constraints
        s = Solver()
        data_store = Const('data_store', data_store_sort)

        s.add(exists(data_store))                                # limit to data stores from the model
        s.add(contains_relevant_evidence(data_store))            # check if data store contains relevant evidence
        s.add(store_id(data_store) != StringVal(data_store_id))  # exclude marked data store
        s.add(pe_number(data_store) != 0)                        # exclude empty data stores

        # Model generation
        solution = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec.name() != 'data_store':  # This is the const with solution
                    continue

                # print(model.decls())
                # print("%s = %s" % (dec.name(), model[dec]))

                # Add a constraint that excludes the current solution from the next iteration
                s.add(store_id(dec()) != store_id(model[dec]))
                # Add the ID of the found data store to the list
                solution.append(str(simplify(store_id(model[dec]))).strip('"'))

        return self.__create_result(solution, data_store_ref_obj.name) if len(solution) > 0 else None
