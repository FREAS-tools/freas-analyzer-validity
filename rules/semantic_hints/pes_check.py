from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from results.response import BPMN4FRSSResponse as Response
from results.warning import BPMN4FRSSWarning
from elements.pool import Pool
from elements.element import Element
from elements.flow.message_flow import MessageFlow


# For all message flows check if the source and target FlowObjects
# have PES label (and if PE is produced)


# If source/target ref is Pool - skipping

@implementer(IRule)
class PotentialEvidenceExists:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        warning = BPMN4FRSSWarning()
        warning.source = solutions
        warning.message = "Flow Objects that are source or target of Message Flow " \
                          "should have Potential Evidence Source label"

        return warning

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (flow object id, has potential evidence source)
        FlowObject, mkFlowObject, (flow_obj_id, has_pes) = TupleSort("FlowObject", [StringSort(), BoolSort()])

        flow_objs = []

        for key, value in elements.items():
            if isinstance(value, MessageFlow):
                source_ref = elements[value.source_ref]
                target_ref = elements[value.target_ref]

                if isinstance(source_ref, Pool) or isinstance(target_ref, Pool):
                    continue

                flow_objs.append(mkFlowObject(StringVal(source_ref.id), source_ref.pe_source is not None))
                flow_objs.append(mkFlowObject(StringVal(target_ref.id), target_ref.pe_source is not None))

        def has_pe_source(source):
            return simplify(has_pes(source))

        def exists(flow_obj):
            return Or([And(flow_obj_id(flow_obj) == flow_obj_id(obj), has_pes(flow_obj) == has_pes(obj)) for obj in
                       flow_objs])

        x = Const('x', FlowObject)
        s.add(Not(has_pe_source(x)))
        s.add(exists(x))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])  # no duplicates
                solutions.append(simplify(flow_obj_id(model[dec])))  # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None
