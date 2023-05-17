from z3 import *
from zope.interface import implementer
from typing import Dict, Optional, List

from rules.rule import IRule
from response.error import Error
from elements.element import Element
from response.severity import Severity
from elements.pot_evidence_source import PotentialEvidenceSource
from response.response import Response


@implementer(IRule)
class MissingPotentialEvidence:
    """
    Rule: Missing Potential Evidence
    Description: This rule checks if Potential Evidence Type is created from Potential Evidence Source.
    """

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = Error()
        error.source = solutions
        error.severity = Severity.HIGH
        error.message = "Data Object with Potential Evidence Type is not created from Potential Evidence Source"

        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # Define Z3 tuple representing Potential Evidence Source, containing the following fields:
        # Potential Evidence Source ID,
        # boolean value indicating whether the Potential Evidence Source has an association
        pe_source_sort, mk_pe_source, (pes_id, has_assoc) = TupleSort("pe_source_sort", [StringSort(), BoolSort()])

        z3_pe_sources = [mk_pe_source(StringVal(value.id), value.association is not None) for _, value in
                         elements.items()
                         if isinstance(value, PotentialEvidenceSource)]

        # Check if potential evidence source has an association
        def has_association(source):
            return simplify(has_assoc(source))

        # Check if potential evidence source exists in the model
        def exists(source):
            return Or([source == elem for elem in z3_pe_sources])

        pe_source = Const('pe_source', pe_source_sort)
        s.add(Not(has_association(pe_source)))
        s.add(exists(pe_source))

        solutions = []
        while s.check() == sat:
            model = s.model()

            for dec in model.decls():
                s.add(dec() != model[dec])                                      # no duplicates
                solutions.append(str(simplify(pes_id(model[dec]))).strip('"'))  # only element's ID

        return self.__create_response(solutions) if len(solutions) > 0 else None
