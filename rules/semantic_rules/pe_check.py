from z3 import *
from zope.interface import implementer
from typing import Dict, Optional, List

from rules.rule import IRule
from results.error import BPMN4FRSSError
from elements.element import Element
from results.severity import Severity
from elements.pot_evidence_source import PotentialEvidenceSource
from results.response import BPMN4FRSSResponse as Response


# Check if potential evidence is missing based on existence of pes
# and association that should be produced from that pes

@implementer(IRule)
class MissingPotentialEvidence:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = BPMN4FRSSError()
        error.source = solutions
        error.severity = Severity.HIGH
        error.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (potential evidence source id, has association)
        PESource, mkPESource, (pes_id, has_assoc) = TupleSort("PESource", [StringSort(), BoolSort()])

        pe_sources = [mkPESource(StringVal(value.id), value.association is not None) for _, value in elements.items()
                      if isinstance(value, PotentialEvidenceSource)]

        # pe_sources += [mkPESource(StringVal("bad"), False)]

        def has_association(source):
            return simplify(has_assoc(source))

        def exists(source):
            return Or([And(pes_id(source) == pes_id(elem), has_assoc(source) == has_assoc(elem)) for elem in pe_sources])

        # s.add([has_association(s) for s in pe_sources])

        x = Const('x', PESource)
        s.add(Not(has_association(x)))
        s.add(exists(x))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])  # no duplicates
                solutions.append(simplify(pes_id(model[dec])))  # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None
