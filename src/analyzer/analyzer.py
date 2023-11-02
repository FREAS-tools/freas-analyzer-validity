from typing import Dict, List

from src.elements.artefact.data_reference import DataStoreReference
from src.elements.element import Element
from src.elements.flow_object.flow_object import FlowObject
from src.input.analysis_types import AnalysisType
from src.input.input import Input
from src.response.response import Response
from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from src.rules.semantic_hints.missing_pes import MissingPES
from src.rules.semantic_hints.reused_key import ReusedKey
from src.rules.semantic_hints.same_evidence_store import SameEvidenceStore

from src.rules.semantic_rules.hash_fun_check import HashFunction
from src.rules.semantic_rules.hash_fun_pes import HashFunctionPES
from src.rules.semantic_rules.keyed_hash_check import KeyedHashFunction


from src.result.result import Result
from src.response.error import Error
from src.response.warning import Warning
from src.rules.semantic_rules.missing_pot_evidence import MissingPotentialEvidence


class Analyzer:
    """
    This class is responsible for performing the analysis.
    It contains a static method analyze, which takes the input parameters and the model elements,
    and returns the result of the analysis.
    """
    @staticmethod
    def analyze(params: Input, elements: Dict[str, Element]) -> Result:
        """
        Performs the analysis on the model elements based on the input parameters.

        Parameters:
            params (Input): Input parameters for the analysis, including the analysis type and optional element id
            elements (Dict[str, Element]): Dictionary of model elements,
            where the key is the element id and the value is the element itself

        Returns:
            Result: Result of the analysis, containing the list of errors, warnings and evidence sources,
            depending on the performed analysis
        """
        result = Result()

        match params.analysis_type:
            case AnalysisType.SEMANTIC_RULES:
                responses = Analyzer.__analyze_semantic_rules(elements)
            case AnalysisType.SEMANTIC_HINTS:
                responses = Analyzer.__analyze_semantic_hints(elements)
            case AnalysisType.EVIDENCE_QUALITY_ANALYSIS:
                responses = Analyzer.__analyze_evidence_quality_rules(elements, params.element_id)
            case _:
                responses = Analyzer.__analyze_semantic_all(elements)

        for response in responses:
            if isinstance(response, Error):
                result.errors.append(response)
            elif isinstance(response, Warning):
                result.warnings.append(response)
            elif isinstance(response, Response):
                result.evidence_sources = response

        return result

    @classmethod
    def __analyze_semantic_rules(cls, elements) -> List[Response]:
        """
        Executes the semantic rules.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Response]: List of responses, containing the Error objects.
        """
        semantic_base_rules = [MissingPotentialEvidence(), HashFunctionPES()]
        passed_base = False
        responses = []

        for rule in semantic_base_rules:
            response = rule.evaluate(elements)

            if response is not None:
                passed_base = False
                responses.append(response)

        # if base rules are not passed, stop the analysis
        if not passed_base:
            return responses

        # INTEGRITY RULES
        rule_groups = [HashFunction(), KeyedHashFunction()]

        for rule in rule_groups:
            responses += rule.evaluate(elements)

        return responses

    @classmethod
    def __analyze_semantic_hints(cls, elements) -> List[Response]:
        """
        Executes the semantic hints.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Response]: List of responses, containing the Warning objects.
        """
        semantic_hints_rules = [MissingPES(), ReusedKey(), SameEvidenceStore()]
        responses = []

        for rule in semantic_hints_rules:
            response = rule.evaluate(elements)

            if response is not None:
                responses.append(response)

        return responses

    @classmethod
    def __analyze_evidence_quality_rules(cls, elements, element_id: str) -> List[Response]:
        """
        Executes the evidence quality rules.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.
            element_id (str): Id of the selected element to be analyzed.

        Returns:
            List[Response]: List containing the one Response object.
        """
        element = elements[element_id]
        rule = None

        if isinstance(element, FlowObject):
            rule = CompromisedFlowObject()
        elif isinstance(element, DataStoreReference):
            rule = CompromisedDataStore()

        response = rule.evaluate(elements, element_id)

        return [response] if response is not None else []

    @classmethod
    def __analyze_semantic_all(cls, elements):
        """
        Executes all the semantic rules and semantic hints.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Response]: List of responses, containing the Error and Warning objects.
        """
        semantic_rules_responses = cls.__analyze_semantic_rules(elements)
        semantic_hints_responses = cls.__analyze_semantic_hints(elements)

        return semantic_rules_responses + semantic_hints_responses
