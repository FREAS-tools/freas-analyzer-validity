from z3 import *

from typing import Dict, List, Optional, Set, Tuple

from src.elements.artefact.data_reference import DataObjectReference, DataStoreReference
from src.elements.frss.evidence_data_relation import EvidenceDataRelation
from src.elements.flow.message_flow import MessageFlow
from src.elements.flow.sequence_flow import SequenceFlow
from src.elements.flow_object.event.catch_event import CatchEvent
from src.elements.frss.evidence_data_store import EvidenceDataStore
from src.elements.flow_object.activity import Activity
from src.elements.flow_object.flow_object import FlowObject
from src.elements.element import Element
from src.elements.flow_object.gateway.gateway import Gateway

from src.rules.utils.semantic import get_participant

"""
This file contains common functionality used by multiple rules for performing evidence quality analysis.
"""


def get_flow_data_objects(elements: Dict[str, Element], flow_obj: Activity) -> Tuple[Set[StringVal], Set[StringVal]]:
    """
    Get altered and unaltered data objects connected to the disputable flow object.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        flow_obj (Activity): Disputable flow object.
    Returns:
        Tuple[Set[StringVal], Set[StringVal]]: A tuple containing two sets of Z3 `StringVal` objects representing data object names.
        The first set contains altered data objects.
        The second set contains potentially unaltered data objects.
    """
    altered_data_objects = set()    # objects being direct output of the flow object
    unaltered_data_objects = set()  # input objects and object connected to the output objects via evidence relation

    has_output_data = False
    for output_assoc in flow_obj.data_output:
        data_object_ref = elements[output_assoc.target_ref]
        if not isinstance(data_object_ref, DataObjectReference):
            continue

        ref_name = data_object_ref.name
        altered_data_objects.add(StringVal(ref_name))
        # Get source data objects connected to the output data object via evidence relation
        unaltered_data_objects |= get_related_evidence(elements, data_object_ref, True)
        has_output_data = True

    for input_assoc in flow_obj.data_input:
        data_object_ref = elements[input_assoc.source_ref]
        if not isinstance(data_object_ref, DataObjectReference):
            continue

        ref_name = data_object_ref.name
        
        # In this case, input data objects are considered altered after the compromised activity is completed 
        if not has_output_data:
            altered_data_objects.add(StringVal(ref_name))
            # Get source data objects connected to the input data object via evidence relation
            unaltered_data_objects |= get_related_evidence(elements, data_object_ref, True)
        else:
            unaltered_data_objects.add(StringVal(ref_name))
            # Get connected data objects with the input data object via evidence relation
            unaltered_data_objects |= get_related_evidence(elements, data_object_ref)

    return altered_data_objects, unaltered_data_objects.difference(altered_data_objects)


def get_related_evidence(elements: Dict[str, Element], data_object_ref: DataObjectReference, 
                         target: bool = False, names: bool = True) -> Set[StringVal]:
    """
    Get all data objects connected to the provided data object or object with the same name via evidence relation.
    Provided data object can be only the relation target (target is true) or both source and target.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        data_object_ref (DataObjectReference): Data object reference.
        target (bool): If true, the provided data object is the relation target, otherwise it can be also source. 
        In case of altered data objects, the provided data object is the relation target.
        names (bool): If true, look also for evidence relations including objects with the same name, 
        otherwise only relations containing provided data object's ID are included.
    Returns:
        Set[StringVal]: A set of Z3 `StringVal` objects representing data object names.
    """
    data_objects = set()  # object connected to the altered objects via evidence relation

    for elem in elements.values():
        if not isinstance(elem, EvidenceDataRelation):
            continue

        if (elem.target_ref == data_object_ref.id or 
            (names and elements[elem.target_ref].name == data_object_ref.name)):
            source_ref = elem.source_ref
            ref_name = elements[source_ref].name
            data_objects.add(StringVal(ref_name))
        
        if not target and (elem.source_ref == data_object_ref.id or 
                           (names and elements[elem.source_ref].name == data_object_ref.name)):
            target_ref = elem.target_ref
            ref_name = elements[target_ref].name
            data_objects.add(StringVal(ref_name))

    return data_objects


def get_sequence_flow_targets(elements: Dict[str, Element], flow_object: FlowObject) -> List[FlowObject]:
    flow_ids = []
    if isinstance(flow_object, Activity) and flow_object.outgoing is not None:
        flow_ids.append(flow_object.outgoing)
    elif isinstance(flow_object, Gateway):
        flow_ids.extend(flow_object.outgoing)

    targets = []
    for flow_id in flow_ids:
        flow: SequenceFlow = elements[flow_id]
        target_id: str = flow.target_ref
        target_obj: FlowObject = elements[target_id]
        targets.append(target_obj)

    return targets


def get_message_flow_target(elements: Dict[str, Element], source: str) -> List[Element]:
    """
    Given a source element ID, returns a list of all target elements of message flow 
    originating from the source element.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        source (str): The ID of the source element.
    Returns:
        List[Element]: A list of all target elements of message flow originating from the source element.
    """
    return [elements[elem.target_ref] for elem in elements.values()
            if isinstance(elem, MessageFlow) and elem.source_ref == source]


def get_disputable_data_stores(elements: Dict[str, Element], flow_obj: Optional[FlowObject],
                               data_stores: List[str]):
    """
    Get all data stores that potentially contain altered data in case of a compromise of the provided flow object.
    (Get all subsequent data stores starting from the provided flow object)
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        flow_obj (Optional[FlowObject]): Flow object.
        data_stores (List[str]): List of data stores.
    Returns:
        List[str]: A list of data stores that are connected to or succeed the provided flow object in the process.
    """
    if flow_obj is None:
        return data_stores

    if isinstance(flow_obj, Activity):
        for assoc in flow_obj.data_output:
            data_ref = elements[assoc.target_ref]

            if isinstance(data_ref, DataStoreReference):
                store_id = data_ref.data
                data_stores.append(StringVal(store_id))

    # Take the following flow object/s
    seq_flow_targets = get_sequence_flow_targets(elements, flow_obj)
    for target in seq_flow_targets:
        get_disputable_data_stores(elements, target, data_stores)

    message_flow_targets = get_message_flow_target(elements, flow_obj.id)
    for message_flow_target in message_flow_targets:
        # Disregard Pool elements
        if isinstance(message_flow_target, FlowObject):
            get_disputable_data_stores(elements, message_flow_target, data_stores)

    return data_stores


def get_potential_evidence(elements: Dict[str, Element], data_store: EvidenceDataStore) -> Set[StringVal]:
    """
    Get all potential evidence objects stored in the provided evidence data store along with the data objects
    connected to them via evidence relations.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        data_store (EvidenceDataStore): Compromised data store.
    Returns:
        Set[StringVal]: A set of Z3 `StringVal` objects representing potential evidence name.

        NOTE: It is necessary to use potential evidence names because more data objects with 
        different IDs can represent the same potential evidence.
    """
    data_objects = set()

    for evidence_id in data_store.stored_pe:
        # Get the data object reference of the evidence
        evidence_name: str = get_data_object_name(elements, evidence_id)
        data_objects.add(StringVal(evidence_name))

        # Add all data objects names connected with evidence relation to the potential evidence
        for elem in elements.values():
            if isinstance(elem, EvidenceDataRelation):
                source: DataObjectReference = elements[elem.source_ref]
                target: DataObjectReference = elements[elem.target_ref]

                if source.data == evidence_id or source.name == evidence_name:
                    data_objects.add(StringVal(target.name))
                elif target.data == evidence_id  or target.name == evidence_name:
                    data_objects.add(StringVal(source.name))

    return data_objects


def get_data_object_reference(elements: Dict[str, Element], data_object: str) -> Optional[DataObjectReference]:
    """
    Get the data object reference of the provided data object.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        data_object (str): data object id.
    Returns:
        Optional[DataObjectReference]: Data object reference object.
    """
    for elem in elements.values():
        if isinstance(elem, DataObjectReference) and elem.data == data_object:
            return elem

    return None


def get_data_object_name(elements: Dict[str, Element], data_object: str) -> str:
    """
    Get the name of the provided data object.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        data_object (str): Data object id.
    Returns:
        str: data object name.
    """
    data_object_ref = get_data_object_reference(elements, data_object)

    assert data_object_ref is not None

    return data_object_ref.name if data_object_ref.name is not None else ""


def get_all_ev_data_stores(elements: Dict[str, Element], mk_data_store) -> List[EvidenceDataStore]:
    """
    Return all evidence data stores from the model in Z3 representation.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
        mk_data_store (Callable): Z3 data store constructor.
    Returns:
        List[EvidenceDataStore]: A list of data stores.
    """
    z3_data_stores = []

    for elem in elements.values():
        if not isinstance(elem, DataStoreReference) or \
           not isinstance(elements[elem.data], EvidenceDataStore):
            continue

        ev_store: EvidenceDataStore = elements[elem.data]
        # Declare a Z3 array for stored potential evidence from the data store
        z3_stored_pe = Array(f"Array_{ev_store.id}", IntSort(), StringSort())

        for i in range(len(ev_store.stored_pe)):
            evidence_id = ev_store.stored_pe[i]
            evidence_name = get_data_object_name(elements, evidence_id)
            # Store potential evidence name to the array
            z3_stored_pe = Store(z3_stored_pe, i, StringVal(evidence_name))

        # Create a Z3 tuple representing the data store
        z3_data_store = mk_data_store(StringVal(ev_store.id), z3_stored_pe, IntVal(len(ev_store.stored_pe)), 
                                      StringVal(get_participant(elements, elem.process_id)))
        z3_data_stores.append(z3_data_store)

    return z3_data_stores

def get_max_number_of_pe(elements: Dict[str, Element]) -> int:
    """
    Get the maximum number of potential evidence stored in a data store.
    Parameters:
        elements (Dict[str, Element]): A dictionary of BPMN4FRSS elements.
    Returns:
        int: Maximum number of potential evidence.
    """
    evidence_count = 0

    for elem in elements.values():
        if isinstance(elem, EvidenceDataStore):
            if len(elem.stored_pe) > evidence_count:
                evidence_count = len(elem.stored_pe)

    return evidence_count
