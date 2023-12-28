from typing import Dict, List

from src.elements.element import Element
from src.elements.flow_object.flow_object import FlowObject
from src.elements.artefact.data_reference import DataStoreReference
from src.analysis_input.analysis_types import AnalysisType
from src.analysis_input.input import Input
from src.analysis_output.output import Output
from src.rules.rule_result.error import Error
from src.rules.rule_result.warning import Warning
from src.rules.rule_result.result import Result
from src.rules.semantic_hints.missing_pes import MissingPES
from src.rules.semantic_rules.missing_evidence import MissingPotentialEvidence
from src.rules.semantic_rules.task_computations.computation_output import ComputationOutput
from src.rules.semantic_rules.task_computations.computation_input import ComputationInput
from src.rules.semantic_hints.computation_pes import ComputationPES
from src.rules.semantic_rules.task_computations.keyed_hash_input import KeyedHashFunInput
from src.rules.semantic_rules.task_computations.keyed_hash_output import KeyedHashFunOutput
from src.rules.evidence_quality_analysis.compromised_data_store import CompromisedDataStore
from src.rules.evidence_quality_analysis.compromised_flow_object import CompromisedFlowObject
from src.rules.semantic_rules.task_computations.integrity_computation_output import IntegrityComputationOutput


class Analyzer:
    """
    This class is responsible for performing the analysis.
    It contains a static method analyze, which takes the input parameters and the model elements,
    and returns the result of the analysis.
    """
    @staticmethod
    def analyze(params: Input, elements: Dict[str, Element]) -> Output:
        """
        Performs the analysis on the model elements based on the input parameters.

        Parameters:
            params (Input): Input parameters for the analysis, including the analysis type and optional element id
            elements (Dict[str, Element]): Dictionary of model elements,
            where the key is the element id and the value is the element itself

        Returns:
            Output: Analysis output, containing the list of errors, warnings and evidence sources,
            depending on the performed analysis
        """
        output = Output()

        match params.analysis_type:
            case AnalysisType.SEMANTIC_RULES:
                results = Analyzer.__analyze_semantic_rules(elements)
            case AnalysisType.SEMANTIC_HINTS:
                results = Analyzer.__analyze_semantic_hints(elements)
            case AnalysisType.SEMANTIC_ALL:
                results = Analyzer.__analyze_semantic_all(elements)
            case AnalysisType.EVIDENCE_QUALITY_ANALYSIS:
                results = Analyzer.__analyze_evidence_quality_rules(elements, params.element_id)

        for result in results:
            if isinstance(result, Error):
                output.errors.append(result)
            elif isinstance(result, Warning):
                output.warnings.append(result)
            elif isinstance(result, Result):
                output.evidence_sources = result

        return output

    @classmethod
    def __analyze_semantic_rules(cls, elements) -> List[Result]:
        """
        Executes the semantic rules.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Result]: List of results, containing the Error objects.
        """

        semantic_rules = [MissingPotentialEvidence(),
                          ComputationInput(), ComputationOutput(), 
                          IntegrityComputationOutput(), KeyedHashFunInput(), KeyedHashFunOutput()]
        results = []

        for rule in semantic_rules:
            result = rule.evaluate(elements)

            if result is not None:
                results.append(result)

        return results

    @classmethod
    def __analyze_semantic_hints(cls, elements) -> List[Result]:
        """
        Executes the semantic hints.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Result]: List of results, containing the Warning objects.
        """
        #semantic_hints_rules = [MissingPES(), ReusedKey(), SameEvidenceStore()]
        semantic_hints_rules = [MissingPES(), ComputationPES()]

        results = []

        for rule in semantic_hints_rules:
            result = rule.evaluate(elements)

            if result is not None:
                results.append(result)

        return results

    @classmethod
    def __analyze_semantic_all(cls, elements):
        """
        Executes all the semantic rules and semantic hints.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.

        Returns:
            List[Result]: List of results, containing the Error and Warning objects.
        """
        semantic_rules_results = cls.__analyze_semantic_rules(elements)
        semantic_hints_results = cls.__analyze_semantic_hints(elements)
        
        return semantic_rules_results + semantic_hints_results

    @classmethod
    def __analyze_evidence_quality_rules(cls, elements, element_id: str) -> List[Result]:
        """
        Executes the evidence quality rules.

        Parameters:
            elements (Dict[str, Element]): Dictionary of model elements.
            element_id (str): Id of the selected element to be analyzed.

        Returns:
            List[Result]: List containing the one result object.
        """
        element = elements[element_id]
        rule = None

        if isinstance(element, FlowObject):
            rule = CompromisedFlowObject()
        elif isinstance(element, DataStoreReference):
            rule = CompromisedDataStore()

        result = rule.evaluate(elements, element_id)

        return [result] if result is not None else []
