from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from rules.rule import IRule
from results.response import Response
from results.recommendation import Recommendation
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
        recommendation = Recommendation()
        recommendation.source = solutions
        recommendation.message = "Flow Objects that are source or target of Message Flow " \
                                 "should have Potential Evidence Source label"

        return recommendation

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        FlowObject, mkFlowObject, (first, second) = TupleSort("FlowObject", [StringSort(), BoolSort()])

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
            return simplify(second(source))

        def exists(flow_obj):
            return Or([And(first(flow_obj) == first(obj), second(flow_obj) == second(obj)) for obj in flow_objs])

        x = Consts('x', FlowObject)
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

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)

        return response
