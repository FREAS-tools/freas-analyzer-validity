from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from src.rules.rule import IRule
from src.rules.rule_result.result import Result
from src.elements.container.pool import Pool
from src.elements.element import Element
from src.elements.flow.message_flow import MessageFlow

from src.rules.z3_types import flow_object_sort, mk_flow_object, flow_obj_id, has_pes

@implementer(IRule)
class MessageFlowPES:
    """
    Rule: Potential Evidence Source on Message Flow
    Description: This rule checks that all Flow Objects that are source or target of Message Flow
    have Potential Evidence Source label.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.message = "Flow Objects that are the source or target element of a Message Flow" \
                          " should have a Potential Evidence Source label."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        # Create a list of all Flow Objects that are the source or target element of a Message Flow
        z3_flow_objects = []

        for key, value in elements.items():
            if isinstance(value, MessageFlow):
                source_ref = elements[value.source_ref]
                target_ref = elements[value.target_ref]

                if isinstance(source_ref, Pool):
                    # A Pool (collapsed) is the source, the target should have PES
                    z3_flow_objects.append(mk_flow_object(StringVal(target_ref.id), target_ref.pe_source is not None))
                elif isinstance(target_ref, Pool):
                    # A Pool (collapsed) is the target, the source should have PES
                    z3_flow_objects.append(mk_flow_object(StringVal(source_ref.id), source_ref.pe_source is not None))
                else:
                    # Both the target and the source should have PES
                    z3_flow_objects.append(mk_flow_object(StringVal(source_ref.id), source_ref.pe_source is not None))
                    z3_flow_objects.append(mk_flow_object(StringVal(target_ref.id), target_ref.pe_source is not None))

        # Check if flow object exists in the model
        def exists(flow_obj):
            return Or([flow_obj == obj for obj in z3_flow_objects])

        # Check if flow object has a Potential Evidence Source label
        def has_pe_source(source):
            return simplify(has_pes(source))

        # Set up the Z3 solver and add the constraints
        s = Solver()
        flow_object = Const('flow_object', flow_object_sort)

        # Tell solver to search for a flow object that does not have a Potential Evidence Source label
        s.add(Not(has_pe_source(flow_object)))
        s.add(exists(flow_object))

        # Model generation
        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                s.add(dec() != model[dec])                                           # no duplicates
                solutions.append(str(simplify(flow_obj_id(model[dec]))).strip('"'))  # only element's ID

        return self.__create_result(solutions) if len(solutions) > 0 else None
