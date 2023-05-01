from z3 import *

from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from elements.data_store import DataStore
from elements.flow_object.flow_object import FlowObject
from elements.element import Element
from results.response import BPMN4FRSSResponse

from rules.utils.disputable import get_flow_data_objects, get_disputable_data_stores


@implementer(IRule)
class CompromisedFlowObject:
    @staticmethod
    def __create_response(solutions: List[str], flow_object) -> BPMN4FRSSResponse:
        response = BPMN4FRSSResponse()
        response.source = solutions
        response.message = "Data Stores that contain potential evidence relevant in " \
                           "case that the flow object \"" + flow_object + "\" is compromised."

        return response

    def evaluate(self, elements: Dict[str, Element], flow_obj_id: str) -> Optional[BPMN4FRSSResponse]:
        s = Solver()

        flow_obj: FlowObject = elements[flow_obj_id]

        # DataStoreArraySort = ArraySort(IntSort(), StringSort())
        DataStoreSort, mkDataStoreSort, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

        # these already contain altered information and do not need to be attacked
        disputable_data_stores = []
        get_disputable_data_stores(elements, flow_obj, disputable_data_stores)

        # possibly altered data objects
        disputable_data_objects = get_flow_data_objects(elements, flow_obj)

        data_stores = []  # slow
        for obj_id, obj in elements.items():
            if not isinstance(obj, DataStore):
                continue

            data_store_obj = Array(f"Array_{obj_id}", IntSort(), StringSort())

            for i in range(len(obj.stored_pe)):
                data_store_obj = Store(data_store_obj, i, StringVal(obj.stored_pe[i]))

            data_store = mkDataStoreSort(StringVal(obj_id), data_store_obj, IntVal(len(obj.stored_pe)))
            data_stores.append(data_store)

        # CONSTRAINTS
        def exists(data_str):
            return Or(
                [And(store_id(data_str) == store_id(store), stored_pe(data_str) == stored_pe(store),
                     pe_number(data_str) == pe_number(store)) for store in data_stores]
            )

        def valid_data_store(data_str):
            return And([store_id(data_str) != store for store in disputable_data_stores])

        # check if at least copy of one disputable data object is stored in the data store
        def contains_relevant_evidence(data_str):
            constraint = []
            for data_obj in disputable_data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj
                                      for i in range(len(disputable_data_objects))]))

            return Or(constraint)

        # MODEL
        x = Consts('x', DataStoreSort)
        s.add(exists(x))
        s.add(valid_data_store(x))
        s.add(contains_relevant_evidence(x))
        s.add(pe_number(x) != 0)

        liability = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec != model.decls()[0]:
                    continue

                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(store_id(dec()) != store_id(model[dec]))  # no duplicates
                liability.append(simplify(store_id(model[dec])))  # only element's ID

        if len(liability) == 0:
            return None

        # print(liability)

        return self.__create_response(liability, flow_obj.name) if len(liability) > 0 else None


# elements = parse("../../docs/diagrams/disputable_stored_in_same_store.bpmn")
# kls = CompromisedFlowObject()
# sol = kls.evaluate(elements, "Activity_1ueekhj")
