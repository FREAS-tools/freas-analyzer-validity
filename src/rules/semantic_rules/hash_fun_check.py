from typing import Dict, List

from src.elements.element import Element
from src.response.response import Response
from src.rules.semantic_rules.hash_fun_input import HashFunctionInput
from src.rules.semantic_rules.hash_fun_output import HashFunctionOutput


class HashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = [HashFunctionInput(), HashFunctionOutput()]
        responses = []

        for rule in rules:
            response = rule.evaluate(elements)
            if response is not None:
                responses.append(response)

        return responses
