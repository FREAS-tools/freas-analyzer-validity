from parser.parser import parse

from rules.flow_check import FlowToItself
from rules.pe_check import MissingPotentialEvidence
from rules.pes_check import PotentialEvidenceExists

from results.result import Result
from results.mistake import Mistake
from results.recommendation import Recommendation


class Analyzer:

    @staticmethod
    def analyze(file_path: str) -> Result:
        elements = parse(file_path)
        result = Result()

        rules = [MissingPotentialEvidence(), FlowToItself(), PotentialEvidenceExists()]

        for rule in rules:
            response = rule.evaluate(elements)

            if response is None:
                continue

            if isinstance(response, Mistake):
                result.mistakes.append(response)
            elif isinstance(response, Recommendation):
                result.recommendations.append(response)

        return result
