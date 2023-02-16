from parser.parser import parse

from rules.flow_check import FlowToItself
from rules.hash_fun_check import CorrectHashFunction
from rules.hash_fun_pes import HashFunctionPES
from rules.keyed_hash_check import CorrectKeyedHashFunction
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

        basic_rules = [MissingPotentialEvidence(), FlowToItself(), PotentialEvidenceExists(), HashFunctionPES()]
        passed_basic = True

        for rule in basic_rules:
            response = rule.evaluate(elements)

            if response is None:
                continue

            passed_basic = False
            if isinstance(response, Mistake):
                result.mistakes.append(response)
            elif isinstance(response, Recommendation):
                result.recommendations.append(response)

        if not passed_basic:
            return result

        rule_groups = [CorrectHashFunction(), CorrectKeyedHashFunction()]
        responses = []

        for rule in rule_groups:
            responses += rule.evaluate(elements)

        for response in responses:
            if isinstance(response, Mistake):
                result.mistakes.append(response)
            elif isinstance(response, Recommendation):
                result.recommendations.append(response)

        return result


# analyzer = Analyzer()
# result = analyzer.analyze("../docs/diagrams/semantics_bad.bpmn")
#
# for mistake in result.mistakes:
#     print(mistake.message)
