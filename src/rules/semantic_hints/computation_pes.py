from z3 import *
from zope.interface import implementer

from typing import Dict, List, Optional

from src.elements.flow_object.task.task import Task
from src.rules.rule import IRule
from src.elements.element import Element
from src.rules.rule_result.result import Result

from src.rules.z3_types import flow_object_sort, mk_flow_object, flow_obj_id, has_pes


@implementer(IRule)
class ComputationPES:
    """
    Rule: Computation Potential Evidence Source
    Description: This rule checks if every computation task has Potential Evidence Source label.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.message = "Task performing computation should have a Potential Evidence Source label."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        z3_tasks = []

        for key, elem in elements.items():
            if isinstance(elem, Task) and elem.computation is not None:
                z3_tasks.append(mk_flow_object(StringVal(key), elem.pe_source is not None))

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
                s.add(dec() != model[dec])                                            # no duplicates
                solutions.append(str(simplify(flow_obj_id(model[dec]))).strip('"'))   # only element's ID

        return self.__create_result(solutions) if len(solutions) > 0 else None
