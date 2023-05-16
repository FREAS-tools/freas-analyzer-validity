from z3 import *

from elements.artefact.data_reference import DataStoreReference

from zope.interface import implementer
from typing import Dict, List, Optional

from response.response import Response
from rules.rule import IRule
from elements.artefact.data_store.data_store import DataStore
from elements.element import Element

from rules.utils.evidence_quality import get_potential_evidence, get_model_data_stores, get_max_number_of_pe


@implementer(IRule)
class CompromisedDataStore:
    """
    Rule: Compromised Data Store
    Description: This rule checks availability of Data Stores that contain potential evidence
    relevant in case of a compromise of the marked Data Store.
    """

    @staticmethod
    def __create_response(solutions: List[str], data_store: str) -> Response:
        response = Response()
        response.source = solutions

        if len(solutions) == 0:
            response.message = "No Data Stores contain potential evidence relevant in " \
                               "case of \"" + data_store + "\" compromise."

        response.message = "Returned Data Stores contain potential evidence relevant in " \
                           "case of \"" + data_store + "\" compromise."

        return response

    def evaluate(self, elements: Dict[str, Element], data_store_ref: str) -> Response:

        data_store_ref_obj: Optional[DataStoreReference] = elements.get(data_store_ref)
        if data_store_ref_obj is None:
            return self.__create_response([], data_store_ref)

        data_store_id: str = data_store_ref_obj.data
        data_store: DataStore = elements[data_store_id]

        # Define the Z3 tuple sort representing data store, containing the following fields:
        # data store ID, array of stored potential evidence and their number
        DataStoreSort, mkDataStoreSort, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

        # Get a list of data object that could indicate data store compromise
        z3_data_objects = get_potential_evidence(elements, data_store)
        # Return the maximum number of potential evidence that is stored in a data store
        max_pe_number = get_max_number_of_pe(elements)

        # Create a list of all data stores present in the model
        z3_data_stores = get_model_data_stores(elements, mkDataStoreSort)

        # CONSTRAINTS
        def exists(data_str):
            return Or(
                [And(store_id(data_str) == store_id(store), stored_pe(data_str) == stored_pe(store),
                     pe_number(data_str) == pe_number(store)) for store in z3_data_stores]
            )

        # check if at least one data object is stored in the data store
        def contains_relevant_evidence(data_str):
            constraint = []
            for data_obj in z3_data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj for i in range(max_pe_number)]))

            return Or(constraint)

        # Set up the Z3 solver and add the constraints
        s = Solver()
        data_store = Consts('data_store', DataStoreSort)

        s.add(exists(data_store))                                # limit to data stores from the model
        s.add(contains_relevant_evidence(data_store))            # check if data store contains relevant evidence
        s.add(store_id(data_store) != StringVal(data_store_id))  # exclude marked data store
        s.add(pe_number(data_store) != 0)                        # exclude empty data stores

        # MODEL
        solution = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec != model.decls()[0]:
                    continue

                # print("%s = %s" % (dec.name(), model[dec]))

                # Add a constraint that excludes the current solution from the next iteration
                s.add(store_id(dec()) != store_id(model[dec]))
                # Add the ID of the found data store to the list
                solution.append(simplify(store_id(model[dec])))

        # print(solution)
        return self.__create_response(solution, data_store_ref_obj.name)


# elements = parse("../../tests/diagrams/disputable_stored_in_same_context_test_1.bpmn")
# kls = CompromisedDataStore()
# sol = kls.evaluate(elements, "DataStoreReference_mydatas_1")
