from z3 import *

from elements.data_object import DataObject
from elements.evidence_data_relation import EvidenceDataRelation
from elements.flow.message_flow import MessageFlow
from elements.flow.sequence_flow import SequenceFlow
from parser.parser import parse

from zope.interface import implementer
from typing import Dict, List, Optional

from results.response import Response
from rules.rule import IRule
from elements.data_store import DataStore
from elements.flow_object.flow_object import FlowObject
from elements.element import Element


@implementer(IRule)
class CompromisedFlowObject:
    @staticmethod
    def __create_response(solutions: List[str], flow_object) -> Response:
        response = Response()
        response.source = solutions
        response.message = "Data Stores that contain potential evidence relevant in " \
                           "case that the flow object \"" + flow_object + "\" is compromised."

        return response

    @staticmethod
    def __get_data_objects(elements: Dict[str, Element], flow_obj: FlowObject):
        data_objects = set()

        for input_assoc in flow_obj.data_input:
            data_object_ref = input_assoc.source_ref  # reference
            data_obj_id = elements[data_object_ref].data
            # add data object that is a direct input to the flow object
            data_objects.add(StringVal(data_obj_id))

            # add also all data objects that have outgoing evidence relation to that data object
            for elem in elements.values():
                if isinstance(elem, EvidenceDataRelation) and elem.target_ref == data_object_ref:
                    source_ref = elem.source_ref
                    data_obj_id = elements[source_ref].data
                    data_objects.add(StringVal(data_obj_id))

        return data_objects

    @staticmethod
    def __get_sequence_flow_target(elements: Dict[str, Element], flow_object: FlowObject) -> Optional[FlowObject]:
        flow_id: Optional[str] = flow_object.outgoing

        if flow_id is None:
            return None

        flow: SequenceFlow = elements[flow_id]
        target_id = flow.target_ref
        target_obj: FlowObject = elements[target_id]

        return target_obj

    @staticmethod
    def __get_message_flow_target(elements: Dict[str, Element], source: str) -> List[Element]:
        return [elements[elem.target_ref] for elem in elements.values()
                if isinstance(elem, MessageFlow) and elem.source_ref == source]

    def __get_disputable_data_stores(self, elements: Dict[str, Element], flow_obj: Optional[FlowObject],
                                     data_stores: List[str]):
        if flow_obj is None:
            return data_stores

        for assoc in flow_obj.data_output:
            data_ref = assoc.target_ref
            data_obj_id = elements[data_ref].data
            data_obj = elements[data_obj_id]

            if isinstance(data_obj, DataStore):
                data_stores.append(StringVal(data_obj_id))

        seq_flow_target = self.__get_sequence_flow_target(elements, flow_obj)
        self.__get_disputable_data_stores(elements, seq_flow_target, data_stores)

        message_flow_targets = self.__get_message_flow_target(elements, flow_obj.id)
        for message_flow_target in message_flow_targets:
            assert isinstance(message_flow_target, FlowObject)

            self.__get_disputable_data_stores(elements, message_flow_target, data_stores)

        return data_stores

    def evaluate(self, elements: Dict[str, Element], flow_obj_id: str) -> Optional[Response]:
        s = Solver()

        flow_obj: FlowObject = elements[flow_obj_id]

        # DataStoreArraySort = ArraySort(IntSort(), StringSort())
        DataStoreSort, mkDataStoreSort, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

        # these already contain altered information and do not need to be attacked
        disputable_data_stores = []
        self.__get_disputable_data_stores(elements, flow_obj, disputable_data_stores)

        # Data Objects that could be stored somewhere with unaltered information
        data_objects = self.__get_data_objects(elements, flow_obj)

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

        # check if at least one data object is stored in the data store
        def contains_relevant_evidence(data_str):
            constraint = []
            for data_obj in data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj for i in range(len(data_objects))]))

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
