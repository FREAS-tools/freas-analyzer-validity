from typing import Dict, List, Optional

from parser.parser import parse

from elements.element import Element
from results.response import Response
from hash_proof_type import HashProofType
from rules.hash_fun_input_type import HashFunctionInputType
from rules.hash_fun_output import HashFunctionOutput


class CorrectHashFunction:

    @staticmethod
    def evaluate(elements: Dict[str, Element]) -> List[Response]:
        rules = [HashFunctionInputType(), HashProofType(), HashFunctionOutput()]
        responses = []

        for rule in rules:
            response = rule.evaluate(elements)
            print(response)
            if response is not None:
                responses.append(response)

        return responses


elements = parse("../docs/diagrams/hash_correct.bpmn")
fun = CorrectHashFunction()
fun.evaluate(elements)
