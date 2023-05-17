from typing import Dict, List

from rules.semantic_rules.keyed_hash_input import KeyedHashFunInput
from rules.semantic_rules.keyed_hash_output import KeyedHashFunOutput
from elements.element import Element
from response.response import Response


class KeyedHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = []
        responses = [KeyedHashFunInput(), KeyedHashFunOutput()]

        for rule in rules:
            response = rule.evaluate(elements)
            # print(response)
            if response is not None:
                responses.append(response)

        return responses
