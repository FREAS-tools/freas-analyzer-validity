from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from elements.flow_object.tasks.task import Task
from rules.rule import IRule
from results.response import Response
from results.error import BPMN4FRSSError
from elements.element import Element


# Check if every Task that executes (Keyed) Hash function has PES label
@implementer(IRule)
class HashFunctionPES:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = BPMN4FRSSError()
        error.source = solutions
        error.message = "Tasks that execute (Keyed) Hash function must have Potential Evidence Source label"

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        TaskSort, mkTaskSort, (first, second) = TupleSort("Task", [StringSort(), BoolSort()])

        tasks = []

        for key, value in elements.items():
            if isinstance(value, Task) and value.hash_fun is not None:
                tasks.append(mkTaskSort(StringVal(key), value.pe_source is not None))

        def has_pe_source(task):
            return simplify(second(task))

        def exists(obj):
            return Or([And(first(task) == first(obj), second(task) == second(obj)) for task in tasks])

        x = Const('x', TaskSort)
        s.add(Not(has_pe_source(x)))
        s.add(exists(x))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])                      # no duplicates
                solutions.append(simplify(first(model[dec])))   # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None
