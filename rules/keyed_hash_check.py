from typing import Dict, List, Optional

from rules.keyed_hash_type import KeyedHashType
from elements.element import Element
from results.response import Response
from hash_fun_check import CorrectHashFunction
from parser.parser import parse


class CorrectKeyedHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = []
        responses = [KeyedHashType()]

        for rule in rules:
            response = rule.evaluate(elements)
            print(response)
            if response is not None:
                responses.append(response)

        return responses


elements = parse("../docs/diagrams/keyed_hash_correct.bpmn")
fun = CorrectHashFunction()
fun.evaluate(elements)
