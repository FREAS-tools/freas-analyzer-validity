from z3 import *

from elements.data_reference import DataObjectReference
from elements.evidence_data_relation import EvidenceDataRelation
from elements.flow.message_flow import MessageFlow
from elements.flow.sequence_flow import SequenceFlow
from typing import Dict, List, Optional

from elements.data_store import DataStore
from elements.flow_object.flow_object import FlowObject
from elements.element import Element


def get_flow_data_objects(elements: Dict[str, Element], flow_obj: FlowObject):
    data_objects = set()

    for input_assoc in flow_obj.data_input:
        data_object_ref = input_assoc.source_ref  # reference
        data_obj_id = elements[data_object_ref].data
        # add data object that is a direct input to the flow object
        data_objects.add(StringVal(data_obj_id))

        # add also all data objects that have outgoing evidence relation to that data object
        for elem in elements.values():
            if isinstance(elem, EvidenceDataRelation) and elem.target_ref == data_object_ref:
                source_ref = elem.source_ref
                data_obj_id = elements[source_ref].data
                data_objects.add(StringVal(data_obj_id))

    return data_objects


def get_sequence_flow_target(elements: Dict[str, Element], flow_object: FlowObject) -> Optional[FlowObject]:
    flow_id: Optional[str] = flow_object.outgoing

    if flow_id is None:
        return None

    flow: SequenceFlow = elements[flow_id]
    target_id = flow.target_ref
    target_obj: FlowObject = elements[target_id]

    return target_obj


def get_message_flow_target(elements: Dict[str, Element], source: str) -> List[Element]:
    return [elements[elem.target_ref] for elem in elements.values()
            if isinstance(elem, MessageFlow) and elem.source_ref == source]


def get_disputable_data_stores(elements: Dict[str, Element], flow_obj: Optional[FlowObject],
                               data_stores: List[str]):
    if flow_obj is None:
        return data_stores

    for assoc in flow_obj.data_output:
        data_ref = assoc.target_ref
        data_obj_id = elements[data_ref].data
        data_obj = elements[data_obj_id]

        if isinstance(data_obj, DataStore):
            data_stores.append(StringVal(data_obj_id))

    seq_flow_target = get_sequence_flow_target(elements, flow_obj)
    get_disputable_data_stores(elements, seq_flow_target, data_stores)

    message_flow_targets = get_message_flow_target(elements, flow_obj.id)
    for message_flow_target in message_flow_targets:
        assert isinstance(message_flow_target, FlowObject)

        get_disputable_data_stores(elements, message_flow_target, data_stores)

    return data_stores


def get_disputable_data_objects(elements: Dict[str, Element], data_store: DataStore):
    data_objects = set()  # data object that could have been altered

    for p_evidence in data_store.stored_pe:
        data_objects.add(StringVal(p_evidence))

        p_evidence_ref: Optional[str] = None
        for elem in elements.values():
            if isinstance(elem, DataObjectReference) and elem.data == p_evidence:
                p_evidence_ref = elem.id
                break

        assert p_evidence_ref is not None

        # add also all data objects that have outgoing evidence relation to that data object
        for elem in elements.values():
            if isinstance(elem, EvidenceDataRelation):
                if elem.source_ref == p_evidence_ref:
                    target_ref = elem.target_ref
                    data_obj_id = elements[target_ref].data
                    data_objects.add(StringVal(data_obj_id))
                elif elem.target_ref == p_evidence_ref:
                    source_ref = elem.source_ref
                    data_obj_id = elements[source_ref].data
                    data_objects.add(StringVal(data_obj_id))

    return data_objects

