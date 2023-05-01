from z3 import *

from elements.data_object import DataObject
from elements.data_reference import DataStoreReference, DataObjectReference
from elements.evidence_data_relation import EvidenceDataRelation
from parser.parser import parse

from zope.interface import implementer
from typing import Dict, List, Optional

from results.response import Response
from rules.rule import IRule
from elements.data_store import DataStore
from elements.flow_object.flow_object import FlowObject
from elements.element import Element


@implementer(IRule)
class CompromisedDataStore:
    @staticmethod
    def __create_response(solutions: List[str], data_store) -> Response:
        response = Response()
        response.source = solutions
        response.message = "Data Stores that contain potential evidence relevant in " \
                           "case that the data store \"" + data_store + "\" is compromised."

        return response

    @staticmethod
    def __get_data_objects(elements: Dict[str, Element], data_store: DataStore):
        data_objects = set()  # data object that could have been altered

        for p_evidence in data_store.stored_pe:
            data_objects.add(StringVal(p_evidence))

            p_evidence_ref: Optional[str] = None
            for elem in elements.values():
                if isinstance(elem, DataObjectReference) and elem.data == p_evidence:
                    p_evidence_ref = elem.id
                    break

            assert p_evidence_ref is not None

            # add also all data objects that have outgoing evidence relation to that data object
            for elem in elements.values():
                if isinstance(elem, EvidenceDataRelation):
                    if elem.source_ref == p_evidence_ref:
                        target_ref = elem.target_ref
                        data_obj_id = elements[target_ref].data
                        data_objects.add(StringVal(data_obj_id))
                    elif elem.target_ref == p_evidence_ref:
                        source_ref = elem.source_ref
                        data_obj_id = elements[source_ref].data
                        data_objects.add(StringVal(data_obj_id))

        return data_objects

    def evaluate(self, elements: Dict[str, Element], data_store_ref: str) -> Optional[Response]:
        s = Solver()

        data_store_ref_obj: DataStoreReference = elements[data_store_ref]
        data_store_id: str = data_store_ref_obj.data
        data_store: DataStore = elements[data_store_id]

        DataStoreSort, mkDataStoreSort, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

        # Data Objects that could be stored somewhere with unaltered information
        data_objects = self.__get_data_objects(elements, data_store)  # problem with duplicates

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

        # check if at least one data object is stored in the data store
        def contains_relevant_evidence(data_str):
            constraint = []
            for data_obj in data_objects:
                constraint.append(Or([Select(stored_pe(data_str), i) == data_obj for i in range(len(data_objects))]))

            return Or(constraint)

        # MODEL
        x = Consts('x', DataStoreSort)
        s.add(exists(x))
        s.add(contains_relevant_evidence(x))
        s.add(store_id(x) != StringVal(data_store_id))  # exclude the marked data store
        s.add(pe_number(x) != 0)  # exclude empty data stores

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
        return self.__create_response(liability, data_store_ref_obj.name) if len(liability) > 0 else None


# elements = parse("../../docs/diagrams/disputable_stored_in_same_store.bpmn")
# kls = CompromisedDataStore()
# sol = kls.evaluate(elements, "DataStoreReference_1qqlqq2")