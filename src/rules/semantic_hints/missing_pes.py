from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from src.rules.rule import IRule
from src.rules.rule_result.result import Result
from src.elements.element import Element
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.frss.potential_evidence_source import PotentialEvidenceSource
from src.elements.frss.evidence_type.potential_evidence_type import PotentialEvidenceType

from src.rules.utils.semantic import get_participant
from src.rules.z3_types import data_object_sort, mk_data_object, participant_id, task_id, object_id, object_name, object_type

@implementer(IRule)
class MissingPES:
    """
    Rule: Missing Potential Evidence Source
    Description: This rule checks that every Potential Evidence has a Potential Evidence Source.
    """

    @staticmethod
    def __create_result(solutions: List[str]) -> Result:
        result = Result()
        result.source = solutions
        result.message = "Potential Evidence should have a Potential Evidence Source."

        return result

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Result]:
        # List of all Potential Evidence Types
        z3_pot_evidence = []

        for _, value in elements.items():
            if isinstance(value, DataObjectReference):
                data_object = elements[value.data]

                if not isinstance(data_object, PotentialEvidenceType):
                    continue
                
                participant = get_participant(elements, data_object.process_id)
                
                z3_evidence = mk_data_object(StringVal(participant), StringVal("None"), StringVal(data_object.id), 
                                StringVal(value.name), StringVal(type(data_object).__name__))

                z3_pot_evidence.append(z3_evidence)
        

        # List of all Potential Evidence Types that have a Potential Evidence Source
        z3_pot_evidence_with_pes = []

        for _, value in elements.items():
            if isinstance(value, PotentialEvidenceSource) and value.association is not None:
                pot_evidence_ref = elements[value.association.target_ref]
                pot_evidence = elements[pot_evidence_ref.data]

                participant = get_participant(elements, pot_evidence.process_id)
                
                z3_evidence = mk_data_object(StringVal(participant), StringVal("None"), StringVal(pot_evidence.id), 
                                StringVal(pot_evidence_ref.name), StringVal(type(pot_evidence).__name__))

                z3_pot_evidence_with_pes.append(z3_evidence)

        # CONSTRAINTS
        def exists(evidence):
            return Or([evidence == pe for pe in z3_pot_evidence])

        def has_pes(evidence):
            return Or([object_name(evidence) == object_name(pe) for pe in z3_pot_evidence_with_pes])
        
        s = Solver()
        evidence = Const('evidence', data_object_sort)

        s.add(exists(evidence))
        s.add(Not(has_pes(evidence)))

        # MODEL
        solutions = []
        while s.check() == sat:
            model = s.model()
            
            solutions.append(str(simplify(object_id(model[evidence]))).strip('"'))
            s.add(And(object_id(evidence) != object_id(model[evidence]), object_name(evidence) != object_name(model[evidence])))

        return self.__create_result(solutions) if len(solutions) > 0 else None
