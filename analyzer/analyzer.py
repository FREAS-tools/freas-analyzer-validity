from typing import Dict, List

from elements.data_reference import DataStoreReference
from elements.element import Element
from elements.flow_object.flow_object import FlowObject
from input.input import BPMN4FRSSInput
from results.response import BPMN4FRSSResponse
from rules.evidence_quality_rules.compromised_data_store import CompromisedDataStore
from rules.evidence_quality_rules.compromised_flow_object import CompromisedFlowObject

from rules.semantic_rules.flow_check import FlowToItself
from rules.semantic_rules.hash_fun_check import HashFunction
from rules.semantic_rules.hash_fun_pes import HashFunctionPES
from rules.semantic_rules.keyed_hash_check import KeyedHashFunction
from rules.semantic_rules.pe_check import MissingPotentialEvidence
from rules.semantic_hints.pes_check import PotentialEvidenceExists

from results.result import Result
from results.error import BPMN4FRSSError
from results.warning import BPMN4FRSSWarning


class Analyzer:

    @staticmethod
    def analyze(params: BPMN4FRSSInput, elements: Dict[str, Element]) -> Result:
        result = Result()

        match params.analysis_type:
            case "SEMANTIC_RULES":
                print("SEMANTIC_RULES")
                responses = Analyzer.__analyze_semantic_rules(elements)
            case "SEMANTIC_HINTS":
                print("SEMANTIC_HINTS")
                responses = Analyzer.__analyze_semantic_hints(elements)
            case "EVIDENCE_QUALITY_ANALYSIS":
                print("EVIDENCE_QUALITY_ANALYSIS")
                responses = Analyzer.__analyze_evidence_quality_rules(elements, params.element_id)
            case _:
                print("SEMANTIC_ALL")
                responses = Analyzer.__analyze_all(elements)

        for response in responses:
            if isinstance(response, BPMN4FRSSError):
                result.errors.append(response)
            elif isinstance(response, BPMN4FRSSWarning):
                result.warnings.append(response)
            elif isinstance(response, BPMN4FRSSResponse):
                result.evidence_sources = response

        return result

    @classmethod
    def __analyze_semantic_rules(cls, elements) -> List[BPMN4FRSSResponse]:
        semantic_base_rules = [MissingPotentialEvidence(), FlowToItself(), HashFunctionPES()]
        passed_base = False
        responses = []

        for rule in semantic_base_rules:
            response = rule.evaluate(elements)

            if response is not None:
                passed_base = False
                responses.append(response)

        if not passed_base:  # if base rules are not passed, stop the analysis
            return responses

        # INTEGRITY RULES
        rule_groups = [HashFunction(), KeyedHashFunction()]

        for rule in rule_groups:
            responses += rule.evaluate(elements)

        return responses

    @classmethod
    def __analyze_semantic_hints(cls, elements):
        semantic_hints_rules = [PotentialEvidenceExists()]
        responses = []

        for rule in semantic_hints_rules:
            response = rule.evaluate(elements)

            if response is not None:
                responses.append(response)

        return responses

    @classmethod
    def __analyze_evidence_quality_rules(cls, elements, element_id: str) -> List[BPMN4FRSSResponse]:
        # evidence_quality_rules = [CompromisedFlowObject(), CompromisedDataStore()]
        # based on the element type, decide which rules to check

        element = elements[element_id]
        rule = None

        if isinstance(element, FlowObject):
            rule = CompromisedFlowObject()
        elif isinstance(element, DataStoreReference):
            rule = CompromisedDataStore()

        response = rule.evaluate(elements, element_id)

        return [response] if response is not None else []

    @classmethod
    def __analyze_all(cls, elements):
        semantic_rules_responses = cls.__analyze_semantic_rules(elements)
        semantic_hints_responses = cls.__analyze_semantic_hints(elements)

        return semantic_rules_responses + semantic_hints_responses
