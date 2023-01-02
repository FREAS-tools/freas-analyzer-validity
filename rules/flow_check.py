from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from elements.flow.flow import Flow
from elements.flow_object.task import Task
from elements.flow_object.event import Event
from elements.element import Element

from results.mistake import Mistake
from results.response import Response
from results.severity import Severity


# Check if there is a flow from task to itself

@implementer(IRule)
class FlowToItself:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.severity = Severity.LOW
        mistake.message = "Flow Object cannot contain Flow to itself"

        return mistake

    def evaluate(self, element: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # Constraint the domain just to the flowObjects
        objs = [obj.id for _, obj in element.items() if isinstance(obj, Task) or isinstance(obj, Event)]
        flowObject, flowObjectValues = EnumSort('flowObject', objs)

        present_flows = []
        for _, value in element.items():
            if isinstance(value, Flow):

                # This extracts the exact value of Sort, corresponding to the name of the flow objects.
                source_ref = next(filter(lambda x: value.source_ref == str(x), flowObjectValues), None)
                target_ref = next(filter(lambda x: value.target_ref == str(x), flowObjectValues), None)
                present_flows.append((source_ref, target_ref))

                if value.target_ref == "Activity_0pfyvl2":
                    present_flows.append((target_ref, target_ref))
                # if value.target_ref == "Event_1o1itgk":
                #     present_flows.append((target_ref, target_ref))

        # This represents the existing flows between flow objects
        # Input two flow objects, return value is True, if there is a flow
        def flow(o1, o2):
            return Or([And(o1 == s, o2 == t) for (s, t) in present_flows])

        # This is the rule, that should not hold in the valid model/diagram
        # If the model is satisfiable with this rule, valuation of f will tell us where exactly is the issue
        f = Const('f', flowObject)
        s.add(flow(f, f))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])  # no duplicates
                solutions.append(model[dec])

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)
        return response
