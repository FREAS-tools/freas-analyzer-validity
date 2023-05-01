from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from elements.flow.flow import Flow
from elements.flow_object.tasks.task import Task
from elements.flow_object.events.event import Event
from elements.element import Element

from results.error import BPMN4FRSSError
from results.response import BPMN4FRSSResponse as Response
from results.severity import Severity


# Check if there is a flow from task to itself

@implementer(IRule)
class FlowToItself:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = BPMN4FRSSError()
        error.source = solutions
        error.severity = Severity.LOW
        error.message = "Flow Object cannot contain Flow to itself"

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # Constraint the domain just to the flowObjects
        objs = [obj.id for _, obj in elements.items() if isinstance(obj, Task) or isinstance(obj, Event)]
        flowObject, flowObjectValues = EnumSort('flowObject', objs)

        present_flows = []
        for _, value in elements.items():
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
            return Or([And(o1 == source, o2 == target) for (source, target) in present_flows])

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

        return self.__create_response(solutions) if len(solutions) > 0 else None
