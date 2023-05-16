from z3 import *

from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from elements.flow_object.flow_object import FlowObject
from elements.element import Element
from response.response import Response

from rules.utils.evidence_quality import get_flow_data_objects, get_disputable_data_stores, get_model_data_stores, \
    get_max_number_of_pe


@implementer(IRule)
class CompromisedFlowObject:
    """
    Rule: Compromised Flow Object
    Description: This rule checks availability of Data Stores that contain potential evidence
    relevant in case of a compromise of the marked Flow Object.
    """

    @staticmethod
    def __create_response(solutions: List[str], flow_object) -> Response:
        response = Response()
        response.source = solutions

        if len(solutions) == 0:
            response.message = "No Data Stores contain potential evidence relevant in " \
                               "case of \"" + flow_object + "\" compromise."

        response.message = "Returned Data Stores contain potential evidence relevant in " \
                           "case of \"" + flow_object + "\" compromise."

        return response

    def evaluate(self, elements: Dict[str, Element], flow_obj_id: str) -> Response:

        flow_obj: Optional[FlowObject] = elements.get(flow_obj_id)
        if flow_obj is None:
            return self.__create_response([], flow_obj_id)

        # Define the Z3 tuple sort representing data stores, containing the following fields:
        # data store ID, array of stored potential evidence and their number
        DataStoreSort, mkDataStoreSort, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

        # these already contain altered information and do not need to be attacked
        disputable_data_stores = []
        get_disputable_data_stores(elements, flow_obj, disputable_data_stores)

        # Get a list of data object that could indicate data store compromise
        #
        z3_altered_data_objects, z3_unaltered_data_objects = get_flow_data_objects(elements, flow_obj)

        z3_data_stores = get_model_data_stores(elements, mkDataStoreSort)
        max_pe_number = get_max_number_of_pe(elements)

        # CONSTRAINTS
        def exists(data_str):
            return Or(
                [And(store_id(data_str) == store_id(store), stored_pe(data_str) == stored_pe(store),
                     pe_number(data_str) == pe_number(store)) for store in z3_data_stores]
            )

        def valid_data_store(data_str):
            return And([store_id(data_str) != store for store in disputable_data_stores])

        # check if at least one piece of potential evidence is stored in the data store
        def has_unaltered_data_object(data_str):
            constraint = []
            for data_obj in z3_unaltered_data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj
                                      for i in range(max_pe_number)]))

            return Or(constraint)

        def has_copy_of_altered_data_object(data_str):
            constraint = []
            for data_obj in z3_altered_data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj
                                      for i in range(max_pe_number)]))

            return Or(constraint)

        s = Solver()
        data_store = Consts('data_store', DataStoreSort)

        s.add(exists(data_store))

        unaltered = And(valid_data_store(data_store), has_copy_of_altered_data_object(data_store))

        altered = has_unaltered_data_object(data_store)
        s.add(Or(unaltered, altered))
        s.add(pe_number(data_store) != 0)

        # MODEL
        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec != model.decls()[0]:
                    continue

                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(store_id(dec()) != store_id(model[dec]))  # no duplicates
                solutions.append(simplify(store_id(model[dec])))  # only element's ID
        # print(solutions)

        return self.__create_response(solutions, flow_obj.name)


# elements = parse("../../documentation/diagrams/disputable_stored_in_same_context_test_1.bpmn")
# kls = CompromisedFlowObject()
# sol = kls.evaluate(elements, "Activity_19xl907")