from z3 import *
from zope.interface import implementer

from typing import List, Dict, Optional

from src.elements.artefact.data_object.data_object import DataObject
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.element import Element
from src.elements.flow_object.task.task import Task
from src.rules.rule_result.result import Result
from src.rules.rule_result.warning import Warning
from src.rules.rule import IRule
from src.elements.frss.forensic_ready_task.computations import HashFunction

from src.rules.utils.semantic import get_participant, get_task_input_object
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, object_name, object_id


@implementer(IRule)
class ReusedKey:
    """
    Rule: Reused key in Keyed Hash Function
    Description: This rules check that a key, which is used in one Keyed Hash Function
    is not being used in a different Pool.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        warning = Warning()
        warning.source = solutions
        warning.message = "The key used in Keyed Hash Function must not be used in different Pool."

        return warning

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        z3_keys = []

        for elem_id, elem in elements.items():
            if not isinstance(elem, Task) or elem.computation is None or \
               not isinstance(elem.computation, HashFunction) or elem.computation.key is None:
                continue

            key = get_task_input_object(elem, elem.computation.key, elements)
            participant = get_participant(elements, key.process_id)

            z3_key = mk_data_object(StringVal(participant), StringVal(elem_id), StringVal(key.id),
                                    StringVal(key.name), StringVal(type(key).__name__))
            z3_keys.append(z3_key)

        # CONSTRAINTS
        def exists(key_obj):
            return Or([key_obj == key for key in z3_keys])

        s = Solver()
        key = Const('key', data_object_sort)
        reused_key = Const('reused_key', data_object_sort)

        s.add(exists(key))
        s.add(exists(reused_key))
        s.add(key != reused_key)

        # The key is considered reused if it has the same name as another key, but different participant ID
        s.add(Not(Distinct(object_name(key), object_name(reused_key))))    # same name
        s.add(Distinct(participant_id(key), participant_id(reused_key)))   # different pool

        # MODEL
        solutions = set()
        while s.check() == sat:
            model = s.model()

            solutions.add(str(simplify(object_id(model[key]))).strip('"'))
            solutions.add(str(simplify(object_id(model[reused_key]))).strip('"'))
            s.add(And(object_id(key) != object_id(model[key]), object_id(key) != object_id(model[reused_key])))

        return self.__create_result(list(solutions)) if len(solutions) > 0 else None
