from z3 import *

from zope.interface import implementer
from typing import Dict, List, Optional

from src.elements.flow_object.activity import Activity
from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.result import Result

from src.rules.z3_types import data_store_sort, mk_data_store, store_id, stored_pe, pe_number
from src.rules.utils.evidence_quality import get_flow_data_objects, get_disputable_data_stores, get_all_ev_data_stores, \
    get_max_number_of_pe


@implementer(IRule)
class CompromisedFlowObject:
    """
    Rule: Compromised Flow Object
    Description: This rule checks availability of Data Stores that contain potential evidence
    relevant in case of a compromise of the marked Flow Object.
    """

    @staticmethod
    def __create_result(solutions: List[str], flow_object: str) -> Result:
        result = Result()
        result.source = solutions

        result.message = "Returned Data Stores contain potential evidence relevant in " \
                           "case that '" + flow_object + "' is compromised."
        return result

    def evaluate(self, elements: Dict[str, Element], flow_obj_id: str) -> Optional[Result]:

        flow_object: Optional[Activity] = elements.get(flow_obj_id)
        if flow_object is None:
            return None

        # Data stores that already contain altered information and do not need to be attacked
        disputable_data_stores = get_disputable_data_stores(elements, flow_object)

        # Get a list of data object that could indicate data store compromise
        z3_altered_data_objects, z3_unaltered_data_objects = get_flow_data_objects(elements, flow_object)

        z3_data_stores = get_all_ev_data_stores(elements, mk_data_store)
        max_pe_number = get_max_number_of_pe(elements)

        # CONSTRAINTS
        def exists(data_str):
            return Or([data_str == store for store in z3_data_stores])

        def valid_data_store(data_str):
            return And([store_id(data_str) != StringVal(store) for store in disputable_data_stores])

        # Check if at least one piece of potential evidence is stored in the data store
        def has_unaltered_data_object(data_str):
            constraint = []
            for data_obj in z3_unaltered_data_objects:
                constraint.append(Or([And(Select(stored_pe(data_str), i) == data_obj, i < pe_number(data_str))
                                      for i in range(max_pe_number)]))

            return Or(constraint)

        # Check if a copy of an altered data object is stored in the data store
        def has_copy_of_altered_data_object(data_str):
            constraint = []
            for data_obj in z3_altered_data_objects:
                constraint.append(Or([And(Select(stored_pe(data_str), i) == data_obj, i < pe_number(data_str))
                                      for i in range(max_pe_number)]))

            return Or(constraint)

        s = Solver()
        data_store = Const('data_store', data_store_sort)

        # Check if a data store that contains the copy (same object name) of potentially altered data object exists.
        # Disregard data stores that contain altered data objects, i.e., data stores subsequent to the flow object.
        copies = And(valid_data_store(data_store), has_copy_of_altered_data_object(data_store))
        # Check if any data store contains data object/s related to the altered data object/s
        unaltered = has_unaltered_data_object(data_store)

        s.add(exists(data_store))
        s.add(Or(copies, unaltered))
        s.add(pe_number(data_store) != 0)   # exclude empty data stores

        # MODEL
        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                if dec.name() != 'data_store':
                    continue

                s.add(store_id(dec()) != store_id(model[dec]))                    # no duplicates
                solutions.append(str(simplify(store_id(model[dec]))).strip('"'))  # only element's ID

        flow_object_name = flow_object.name if flow_object.name is not None else flow_object.id
        
        return self.__create_result(solutions, flow_object_name) if solutions else None
