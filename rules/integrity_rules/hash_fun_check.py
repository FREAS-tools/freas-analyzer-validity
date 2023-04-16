from typing import Dict, List

from parser.parser import parse

from elements.element import Element
from results.response import Response
from rules.integrity_rules.hash_fun_input import HashFunctionInput
from rules.integrity_rules.hash_fun_output import HashFunctionOutput


class HashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = [HashFunctionInput(), HashFunctionOutput()]
        responses = []

        for rule in rules:
            response = rule.evaluate(elements)
            print(response)
            if response is not None:
                responses.append(response)

        return responses


elements = parse("../../docs/diagrams/hash_correct.bpmn")
fun = HashFunction()
fun.evaluate(elements)
