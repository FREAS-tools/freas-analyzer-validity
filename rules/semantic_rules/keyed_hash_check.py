from typing import Dict, List

from rules.semantic_rules.keyed_hash_input import KeyedHashFunInput
from rules.semantic_rules.keyed_hash_output import KeyedHashFunOutput
from elements.element import Element
from results.response import Response
from parser.parser import parse


class KeyedHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = []
        responses = [KeyedHashFunInput(), KeyedHashFunOutput()]

        for rule in rules:
            response = rule.evaluate(elements)
            print(response)
            if response is not None:
                responses.append(response)

        return responses


elements = parse("../../docs/diagrams/keyed_hash_correct.bpmn")
fun = KeyedHashFunction()
fun.evaluate(elements)
