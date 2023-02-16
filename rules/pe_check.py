from z3 import *
from zope.interface import implementer
from typing import Dict, Optional, List

from rules.rule import IRule
from results.mistake import Mistake
from elements.element import Element
from results.response import Response
from results.severity import Severity
from elements.pe_source import PotentialEvidenceSource


# Check if potential evidence is missing based on existence of pes
# and association that should be produced from that pes

@implementer(IRule)
class MissingPotentialEvidence:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.severity = Severity.HIGH
        mistake.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"

        return mistake

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors
        PESource, mkPESource, (first, second) = TupleSort("PESource", [StringSort(), BoolSort()])

        pe_sources = [mkPESource(StringVal(value.id), value.association is not None) for _, value in elements.items()
                      if isinstance(value, PotentialEvidenceSource)]

        # pe_sources += [mkPESource(StringVal("bad"), False)]

        def has_association(source):
            return simplify(second(source))

        def exists(source):
            return Or([And(first(source) == first(elem), second(source) == second(elem)) for elem in pe_sources])

        # s.add([has_association(s) for s in pe_sources])

        x = Consts('x', PESource)
        s.add(Not(has_association(x)))
        s.add(exists(x))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                # print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])  # no duplicates
                solutions.append(simplify(first(model[dec])))  # only element's ID

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)

        return response
