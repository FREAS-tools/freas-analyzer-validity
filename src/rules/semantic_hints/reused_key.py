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

from src.rules.utils.semantic import get_participant
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, object_name


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
            if not isinstance(elem, Task) or elem.hash_fun is None or elem.hash_fun.key is None:
                continue

            key_ref: DataObjectReference = elements[elem.hash_fun.key]
            key: DataObject = elements[key_ref.data]
            participant = get_participant(elements, key.process_id)

            z3_key = mk_data_object(StringVal(participant), StringVal(elem_id), StringVal(key.id),
                                    StringVal(key_ref.name), StringVal(type(key).__name__))
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

        # The key is reused if it has the same key ID and key name, but different participant ID
        s.add(Not(Distinct(object_name(key), object_name(reused_key))))    # same key
        s.add(Distinct(participant_id(key), participant_id(reused_key)))   # different pool

        # MODEL
        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                s.add(participant_id(dec()) != participant_id(model[dec]))              # no duplicates
                solutions.append(str(simplify(participant_id(model[dec]))).strip('"'))  # only element's ID
                break

        return self.__create_result(solutions) if len(solutions) > 0 else None
