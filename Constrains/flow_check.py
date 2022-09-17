from Elements.Flow.flow import Flow
from Elements.Element.element import Element

from Constrains.base_sorts import *

from typing import Dict


# Check if there is a flow from task to itself

def check_flow(elem: Dict[str, Element]) -> Solver:
    # set_param(proof=True)

    s = Solver()
    # s.set(unsat_core=True)
    # s.set(proof=True)
    flow = Function("flow", FlowObjSort, FlowObjSort, BoolSort())
    flow_obj = Const("flow_obj", FlowObjSort)
    s.add(ForAll(flow_obj, Not(flow(flow_obj, flow_obj))))
    # s.add(Not(Exists(flow_obj, flow(flow_obj, flow_obj))))
    # s.add(flow(flow_obj, flow_obj))

    for key, value in elem.items():
        if isinstance(value, Flow):
            target_ref = Const(value.target_ref, FlowObjSort)
            source_ref = Const(value.source_ref, FlowObjSort)
            s.add(flow(target_ref, source_ref))
            solve(Not(flow(target_ref, target_ref)))
            # if value.target_ref == "Activity_0pfyvl2":
            #     s.add(flow(target_ref, target_ref))


    # print(s.check(Exists(flow_obj, flow(flow_obj, flow_obj))))
    # print(s.check())
    # print(s.unsat_core())
    # print()
    # print(s.proof())

    return s
