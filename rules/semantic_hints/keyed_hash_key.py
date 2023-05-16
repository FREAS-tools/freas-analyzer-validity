from typing import List, Dict, Optional

from z3 import *
from zope.interface import implementer

from elements.element import Element
from elements.flow_object.task.task import Task
from response.response import Response
from response.warning import Warning
from rules.rule import IRule
from rules.utils.semantic import get_participant


@implementer(IRule)
class ReusedKeyedHashKey:
    """
    Rule: Unique key in KeyedHashFunction
    Description: The key used in KeyedHashFunction MUST not be used in different Pool.
    Output:
    """

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        warning = Warning()
        warning.source = solutions
        warning.message = "The key used in KeyedHashFunction MUST not be used in different Pool."

        return warning

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:

        # The sort, a constructor, and the accessors (participant id, data object id, data object type)
        KeySort, mkKey, (participant_id, key_id, key_name) = \
            TupleSort("Key", [StringSort(), StringSort(), StringSort()])

        z3_keys = []
        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.hash_fun is None or elem.hash_fun.key is None:
                continue

            key_ref = elements[elem.hash_fun.key]
            key = elements[key_ref.data]
            participant = get_participant(elements, key.process_id)

            z3_key = mkKey(StringVal(participant), StringVal(key.id), StringVal(key_ref.name))
            z3_keys.append(z3_key)

        # CONSTRAINTS
        def exists(key_obj):
            return Or(
                [And(key_id(key_obj) == key_id(k), participant_id(key_obj) == participant_id(k),
                     key_name(key_obj) == key_name(k)) for k in z3_keys]
            )

        s = Solver()
        key = Const('key', KeySort)
        reused_key = Const('dup_key', KeySort)

        s.add(exists(key))
        s.add(exists(reused_key))
        s.add(key != reused_key)

        s.add(Not(Distinct(key_name(key), key_name(reused_key))))  # same key
        s.add(Distinct(participant_id(key), participant_id(reused_key)))   # different pool

        # MODEL
        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(participant_id(dec()) != participant_id(model[dec]))  # no duplicates
                solutions.append(simplify(participant_id(model[dec])))  # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None


