from typing import Dict

from elements.element import Element
from results.response import Response
from rules.global_rules.flow_check import FlowToItself
from rules.integrity_rules.hash_fun_check import HashFunction
from rules.global_rules.hash_fun_pes import HashFunctionPES
from rules.integrity_rules.keyed_hash_check import KeyedHashFunction
from rules.global_rules.pe_check import MissingPotentialEvidence
from rules.global_rules.pes_check import PotentialEvidenceExists

from results.result import Result
from results.error import BPMN4FRSSError
from results.warning import BPMN4FRSSWarning


class Analyzer:

    @staticmethod
    def analyze(elements: Dict[str, Element]) -> Result:
        result = Result()

        basic_rules = [MissingPotentialEvidence(), FlowToItself(), PotentialEvidenceExists(), HashFunctionPES()]
        passed_basic = True

        # GLOBAL RULES
        for rule in basic_rules:
            response = rule.evaluate(elements)

            if response is None:
                continue

            passed_basic = False
            if isinstance(response, BPMN4FRSSError):
                result.errors.append(response)
            elif isinstance(response, BPMN4FRSSWarning):
                result.warnings.append(response)

        if not passed_basic:
            return result

        # INTEGRITY RULES
        rule_groups = [HashFunction(), KeyedHashFunction()]
        responses = []

        for rule in rule_groups:
            responses += rule.evaluate(elements)

        # EVIDENCE QUALITY ANALYSIS
        # TODO

        for response in responses:
            if isinstance(response, BPMN4FRSSError):
                result.errors.append(response)
            elif isinstance(response, BPMN4FRSSWarning):
                result.warnings.append(response)
            elif isinstance(response, Response):
                result.evidence_stores.append(response)

        return result
