from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from src.elements.flow_object.task.task import Task
from src.rules.rule_result.severity import Severity
from src.rules.rule import IRule
from src.rules.rule_result.error import Error
from src.elements.element import Element
from src.rules.rule_result.result import Result

from src.rules.z3_types import flow_object_sort, mk_flow_object, flow_obj_id, has_pes


@implementer(IRule)
class HashFunctionPES:
    """
    Rule: Hash Function and Potential Evidence Source
    Description: This rule checks if every Task that executes (Keyed) Hash function has Potential Evidence Source label.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        error = Error()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Tasks that execute (Keyed) Hash function must have Potential Evidence Source label"

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        z3_tasks = []

        # Collect all tasks that have hash_fun
        for key, value in elements.items():
            if isinstance(value, Task) and value.hash_fun is not None:
                z3_tasks.append(mk_flow_object(StringVal(key), value.pe_source is not None))

        def has_pe_source(task):
            return simplify(has_pes(task))

        def exists(obj):
            return Or([obj == task for task in z3_tasks])

        s = Solver()
        z3_task = Const('z3_task', flow_object_sort)

        # Constraints
        s.add(Not(has_pe_source(z3_task)))
        s.add(exists(z3_task))

        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                s.add(dec() != model[dec])                                      # no duplicates
                solutions.append(str(simplify(flow_obj_id(model[dec]))).strip('"'))   # only element's ID

        return self.__create_result(solutions) if len(solutions) > 0 else None
