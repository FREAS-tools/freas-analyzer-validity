from typing import Dict, List

from src.rules.semantic_rules.keyed_hash_input import KeyedHashFunInput
from src.rules.semantic_rules.keyed_hash_output import KeyedHashFunOutput
from src.elements.element import Element
from src.rules.rule_result.result import Result


class KeyedHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Result]:
        rules = []
        results = [KeyedHashFunInput(), KeyedHashFunOutput()]

        for rule in rules:
            result = rule.evaluate(elements)
            
            if result is not None:
                results.append(result)

        return results
