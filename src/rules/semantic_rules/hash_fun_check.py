from typing import Dict, List

from src.elements.element import Element
from src.rules.rule_result.result import Result
from src.rules.semantic_rules.hash_fun_input import HashFunctionInput
from src.rules.semantic_rules.hash_fun_output import HashFunctionOutput


class HashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Result]:
        rules = [HashFunctionInput(), HashFunctionOutput()]
        results = []

        for rule in rules:
            result = rule.evaluate(elements)
            if result is not None:
                results.append(result)

        return results
