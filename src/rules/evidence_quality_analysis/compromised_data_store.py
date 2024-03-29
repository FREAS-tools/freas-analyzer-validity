from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.rules.rule_result.result import Result
from src.rules.rule import IRule
from src.elements.frss.evidence_data_store import EvidenceDataStore
from src.elements.element import Element
from src.elements.artefact.data_reference import DataStoreReference

from src.rules.z3_types import data_store_sort, mk_data_store, store_id, stored_pe, pe_number
from src.rules.utils.evidence_quality import get_potential_evidence, get_all_ev_data_stores


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
                         "case that '" + data_store + "' is compromised."

        return result

    def evaluate(self, elements: Dict[str, Element], data_store_ref: str) -> Optional[Result]:

        data_store_ref_obj: Optional[DataStoreReference] = elements.get(data_store_ref)
        if data_store_ref_obj is None:
            return None

        data_store_id: str = data_store_ref_obj.data
        data_store = elements[data_store_id]

        if not isinstance(data_store, EvidenceDataStore):
            return None

        # Get a list of potential evidence names that could indicate data store compromise
        z3_evidence = get_potential_evidence(elements, data_store)

        # Create a list of all data stores present in the model
        z3_data_stores = get_all_ev_data_stores(elements, mk_data_store)

        # Check if the data store exists in the model
        def exists(data_str):
            return Or([data_str == store for store in z3_data_stores])

        # Checks if there exists an index such that the array at that index contains the potential evidence
        def contains_evidence(index, data_str):
            return Exists(index,
                          Or([  # at least one of the potential evidence is stored in the data store
                              And(
                                  Select(stored_pe(data_str), index) == data_obj,
                                  # the array at the index contains the potential evidence
                                  0 <= index,  # index is not negative
                                  index < pe_number(data_str)
                                  # index is not larger than the number of stored potential evidence
                              )
                              for data_obj in z3_evidence
                          ])
                        )

        # Set up the Z3 solver and add the constraints
        s = Solver()
        data_store = Const('data_store', data_store_sort)
        index = Int('index')

        s.add(exists(data_store))  # limit to data stores from the model
        s.add(contains_evidence(index, data_store))  # at least one potential evidence needs to be stored
        s.add(store_id(data_store) != StringVal(data_store_id))  # exclude marked data store

        # Model generation
        solution = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec.name() != 'data_store':  # This is the const with solution
                    continue

                # Add a constraint that excludes the current solution from the next iteration
                s.add(store_id(dec()) != store_id(model[dec]))
                # Add the ID of the found data store to the list
                solution.append(str(simplify(store_id(model[dec]))).strip('"'))
        
        data_store_name = data_store_ref_obj.name if data_store_ref_obj.name is not None else data_store_ref_obj.id

        return self.__create_result(solution, data_store_name) if len(solution) > 0 else None
