from typing import Dict, List

from src.rules.semantic_rules.keyed_hash_input import KeyedHashFunInput
from src.rules.semantic_rules.keyed_hash_output import KeyedHashFunOutput
from src.elements.element import Element
from src.response.response import Response


class KeyedHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = []
        responses = [KeyedHashFunInput(), KeyedHashFunOutput()]

        for rule in rules:
            response = rule.evaluate(elements)
            
            if response is not None:
                responses.append(response)

        return responses
