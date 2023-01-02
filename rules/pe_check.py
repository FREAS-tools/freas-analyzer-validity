from elements.pe_source import PotentialEvidenceSource
from elements.element import Element

from rules.base_sorts import *

from typing import Dict


# Check if potential evidence is missing based on existence of pes
# and association that should be produced from that pes


def check_pe(elem: Dict[str, Element]) -> Solver:
    s = Solver()

    has_association = Function("has_association", PESourceSort, BoolSort())
    pe_source = Const("pe_source", PESourceSort)
    s.add(ForAll(pe_source, has_association(pe_source)))

    for key, value in elem.items():
        if isinstance(value, PotentialEvidenceSource):
            pes = Const(value.id, PESourceSort)

            if value.association is not None:
                s.add(has_association(pes))
            else:
                s.add(Not(has_association(pes)))

    return s
