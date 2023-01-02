from elements.element import Element
from elements.flow.message_flow import MessageFlow
from elements.flow_object.flow_object import FlowObject

from rules.base_sorts import *

from typing import Dict

# For all message flows check if the source_ref and target_ref (FlowObjects)
# have PES label and if PE is produced


def check_pes(elements: Dict[str, Element]) -> Solver:
    s = Solver()

    has_pe_source = Function("has_pe_source", FlowObjSort, BoolSort())
    flow_obj = Const("pe_source", FlowObjSort)
    s.add(ForAll(flow_obj, has_pe_source(flow_obj)))

    for key, value in elements.items():
        if isinstance(value, MessageFlow):
            source_ref = elements[value.source_ref]
            add_constrain(source_ref, has_pe_source, s)

            target_ref = elements[value.target_ref]
            add_constrain(target_ref, has_pe_source, s)

    return s


def add_constrain(elem, has_pe_source, s):
    if isinstance(elem, FlowObject):  # it can also be a Pool
        flow_object = Const(elem.id, FlowObjSort)
        if elem.pe_source is not None:
            s.add(has_pe_source(flow_object))
        else:
            s.add(Not(has_pe_source(flow_object)))
