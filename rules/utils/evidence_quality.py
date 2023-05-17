from z3 import *

from elements.artefact.data_reference import DataObjectReference
from elements.artefact.data_object.evidence_data_relation import EvidenceDataRelation
from elements.flow.message_flow import MessageFlow
from elements.flow.sequence_flow import SequenceFlow
from typing import Dict, List, Optional, Set, Tuple

from elements.artefact.data_store.data_store import DataStore
from elements.flow_object.activity import Activity
from elements.flow_object.flow_object import FlowObject
from elements.element import Element
from elements.flow_object.gateway.gateway import Gateway

"""
This file contains common functionality used by multiple rules when performing evidence quality analysis.
"""


def get_flow_data_objects(elements: Dict[str, Element], flow_obj: Activity) -> Tuple[Set[StringVal], Set[StringVal]]:
    altered_data_objects = set()
    unaltered_data_objects = set()

    for output_assoc in flow_obj.data_output:
        data_object_ref = output_assoc.target_ref  # reference
        if not isinstance(elements[data_object_ref], DataObjectReference):
            continue

        ref_name = elements[data_object_ref].name
        altered_data_objects.add(StringVal(ref_name))

        for elem in elements.values():
            if isinstance(elem, EvidenceDataRelation) and elem.target_ref == data_object_ref:
                source_ref = elem.source_ref
                ref_name = elements[source_ref].name
                unaltered_data_objects.add(StringVal(ref_name))

    return altered_data_objects, unaltered_data_objects


def get_sequence_flow_targets(elements: Dict[str, Element], flow_object: FlowObject) -> List[FlowObject]:
    flow_ids = []
    if isinstance(flow_object, Activity) and flow_object.outgoing is not None:
        flow_ids = [flow_object.outgoing]
    elif isinstance(flow_object, Gateway):
        flow_ids = flow_object.outgoing

    targets = []
    for flow_id in flow_ids:
        flow: SequenceFlow = elements[flow_id]
        target_id: str = flow.target_ref
        target_obj: FlowObject = elements[target_id]
        targets.append(target_obj)

    # print("targets", targets)
    return targets


def get_message_flow_target(elements: Dict[str, Element], source: str) -> List[Element]:
    return [elements[elem.target_ref] for elem in elements.values()
            if isinstance(elem, MessageFlow) and elem.source_ref == source]


def get_disputable_data_stores(elements: Dict[str, Element], flow_obj: Optional[FlowObject],
                               data_stores: List[str]):
    if flow_obj is None:
        return data_stores

    if isinstance(flow_obj, Activity):
        for assoc in flow_obj.data_output:
            data_ref = assoc.target_ref
            data_obj_id = elements[data_ref].data
            data_obj = elements[data_obj_id]

            if isinstance(data_obj, DataStore):
                data_stores.append(StringVal(data_obj_id))

    # print("calling with ", flow_obj.id)
    seq_flow_targets = get_sequence_flow_targets(elements, flow_obj)
    # print("main fun after get seq")
    for target in seq_flow_targets:
        get_disputable_data_stores(elements, target, data_stores)

    message_flow_targets = get_message_flow_target(elements, flow_obj.id)
    for message_flow_target in message_flow_targets:
        if isinstance(message_flow_target, FlowObject):
            get_disputable_data_stores(elements, message_flow_target, data_stores)

    return data_stores


def get_potential_evidence(elements: Dict[str, Element], data_store: DataStore) -> Set[StringVal]:
    """
    Get all data object stored in the provided data store along with the data objects
    connected to them via evidence relations.
    Parameters:
        elements (Dict[str, Element]): model elements.
        data_store (DataStore): compromised data store.
    Returns:
        Set[StringVal]: A set of Z3 `StringVal` objects representing data object name.
    """
    data_objects = set()

    for evidence_id in data_store.stored_pe:
        # Get the data object reference of the evidence
        pot_evidence_ref: Optional[DataObjectReference] = get_data_object_reference(elements, evidence_id)

        if pot_evidence_ref is None:
            continue

        data_objects.add(StringVal(pot_evidence_ref.name))

        # Add all data objects names connected with evidence relation to the potential evidence
        for elem in elements.values():
            if isinstance(elem, EvidenceDataRelation):
                if elem.source_ref == pot_evidence_ref.id:
                    target_ref = elem.target_ref
                    ref_name = elements[target_ref].name
                    data_objects.add(StringVal(ref_name))
                elif elem.target_ref == pot_evidence_ref.id:
                    source_ref = elem.source_ref
                    ref_name = elements[source_ref].name
                    data_objects.add(StringVal(ref_name))

    return data_objects


def get_data_object_reference(elements: Dict[str, Element], data_object: str) -> Optional[DataObjectReference]:
    """
    Get the data object reference of the provided data object.
    Parameters:
        elements (Dict[str, Element]): model elements.
        data_object (str): data object id.
    Returns:
        Optional[DataObjectReference]: data object reference object.
    """
    for elem in elements.values():
        if isinstance(elem, DataObjectReference) and elem.data == data_object:
            return elem

    return None


def get_data_object_name(elements: Dict[str, Element], data_object: str) -> str:
    """
    Get the name of the provided data object.
    Parameters:
        elements (Dict[str, Element]): model elements.
        data_object (str): data object id.
    Returns:
        str: data object name.
    """
    data_object_ref = get_data_object_reference(elements, data_object)

    assert data_object_ref is not None

    return data_object_ref.name if data_object_ref.name is not None else ""


def get_model_data_stores(elements: Dict[str, Element], constructor) -> List[DataStore]:
    """
    Return all data stores from the model in Z3 representation.
    Parameters:
        elements (Dict[str, Element]): model elements.
        constructor (Callable): Z3 data store constructor.
    Returns:
        List[DataStore]: A list of data stores.
    """
    z3_data_stores = []

    for elem_id, elem in elements.items():
        if not isinstance(elem, DataStore):
            continue

        # Declare a Z3 array for stored potential evidence from the data store
        z3_stored_pe = Array(f"Array_{elem_id}", IntSort(), StringSort())

        for i in range(len(elem.stored_pe)):
            evidence_id = elem.stored_pe[i]
            pot_evidence_name = get_data_object_name(elements, evidence_id)
            # Add stored potential evidence name to the array
            z3_stored_pe = Store(z3_stored_pe, i, StringVal(pot_evidence_name))

        # Create a Z3 tuple representing the data store
        z3_data_store = constructor(StringVal(elem_id), z3_stored_pe, IntVal(len(elem.stored_pe)))
        z3_data_stores.append(z3_data_store)

    return z3_data_stores


def get_max_number_of_pe(elements: Dict[str, Element]) -> int:
    """
    Get the maximum number of potential evidence stored in a data store.
    Parameters:
        elements (Dict[str, Element]): model elements.
    Returns:
        int: maximum number of potential evidence.
    """
    max_pe = 0

    for elem in elements.values():
        if isinstance(elem, DataStore):
            if len(elem.stored_pe) > max_pe:
                max_pe = len(elem.stored_pe)

    return max_pe
