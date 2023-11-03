import xml.etree.ElementTree as ET

from src.elements.artefact.data_object.pot_evidence_type import PotentialEvidenceType
from src.elements.container.pool import Pool
from src.elements.container.process import Process
from src.elements.element import Element
from src.elements.artefact.data_store.data_store import DataStore
from src.elements.flow_object.event.throw_event import EndEvent
from src.elements.flow_object.gateway.gateway import ExclusiveGateway, Gateway
from src.elements.flow_object.task.task import Task
from src.elements.flow.message_flow import MessageFlow
from src.elements.flow.sequence_flow import SequenceFlow
from src.elements.pot_evidence_source import PotentialEvidenceSource
from src.elements.flow_object.flow_object import FlowObject
from src.elements.flow_object.hash_function import HashFunction
from src.elements.artefact.data_object.evidence_data_relation import EvidenceDataRelation
from src.elements.artefact.data_reference import DataObjectReference, DataStoreReference
from src.elements.artefact.data_object.data_object import DataObject
from src.elements.artefact.data_object.proof import HashProof, KeyedHashProof
from src.elements.flow_object.event.catch_event import StartEvent, IntermediateCatchEvent
from src.elements.flow_object.task.association import Association, DataInputAssociation, DataOutputAssociation

from typing import Dict

"""
Responsible for parsing BPMN4FRSS XML file into a dictionary of elements.
"""


def get_tag(elem: ET.Element) -> str:  # without namespace
    tag_list = elem.tag.split('}')

    if len(tag_list) > 1:
        return tag_list[1]
    return tag_list[0]


def parse_collaboration(elem: ET.Element, elements: Dict[str, Element]):
    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        new_elem = None

        match tag:
            case 'participant':
                new_elem = Pool(attr['id'], attr['processRef'], attr.get('name'))
            case 'messageFlow':
                new_elem = MessageFlow(attr['id'], attr['sourceRef'],
                                       attr['targetRef'], attr.get('name'))
                
        store_element(new_elem, elements)


def get_source_target_ref(elem: ET.Element):
    source, target = None, None

    for child in elem:
        tag = get_tag(child)
        if tag == "sourceRef":
            source = child.text
        if tag == "targetRef":
            target = child.text

    return source, target


def parse_flow_object(elem: ET.Element, obj: FlowObject) -> FlowObject:
    obj.name = elem.attrib.get('name')

    for child in elem:
        tag = get_tag(child)

        match tag:
            case "incoming":
                if isinstance(obj, Gateway):
                    obj.incoming.append(child.text)
                else:
                    obj.incoming = child.text
            case "outgoing":
                if isinstance(obj, Gateway):
                    obj.outgoing.append(child.text)
                else:
                    obj.outgoing = child.text
            case "dataOutputAssociation":
                _, target = get_source_target_ref(child)
                association = DataOutputAssociation(child.attrib['id'], obj.id, target)
                obj.data_output.append(association)
            case "dataInputAssociation":
                source, _ = get_source_target_ref(child)
                association = DataInputAssociation(child.attrib['id'], source, obj.id)
                obj.data_input.append(association)
            case "hashFunction":
                obj.hash_fun = HashFunction(child.attrib.get('input'), child.attrib.get('output'))
            case "keyedHashFunction":
                obj.hash_fun = HashFunction(child.attrib.get('input'), child.attrib.get('output'),
                                            child.attrib.get('key'))

    return obj


def parse_data_object(elem: ET.Element, process_id: str) -> DataObject:
    for child in elem:
        tag = get_tag(child)
        if tag == "potentialEvidence":
            return PotentialEvidenceType(elem.attrib['id'], process_id)
        if tag == "hash":
            return HashProof(elem.attrib['id'], process_id)
        if tag == "keyedHash":
            return KeyedHashProof(elem.attrib['id'], process_id)

    return DataObject(elem.attrib['id'], process_id)


def parse_data_store(elem: ET.Element) -> DataStore:
    data_store = DataStore(elem.attrib['id'])

    for child in elem:
        tag = get_tag(child)
        if tag == "evidenceDataStore":
            for sub_child in child:
                subtag = get_tag(sub_child)
                if subtag == "stores":
                    data_store.stored_pe.append(sub_child.text)
            break

    return data_store


def add_pe_source(pe_source, elements: Dict[str, Element]):
    key = pe_source.attached_to_ref  # object id

    if elements.get(key) is not None:
        obj = elements[key]
        obj.pe_source = pe_source


def attach_association(association: Association, elements:  Dict[str, Element]):
    pe_source_id = association.source_ref
    pe_source = elements.get(pe_source_id)
    pe_source.association = association if pe_source else None


def parse_process(elem: ET.Element, elements: Dict[str, Element]):
    process = Process(elem.attrib['id'])
    elements[process.id] = process

    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        new_elem = None

        match tag:
            case "task":
                task = Task(attr['id'])
                new_elem = parse_flow_object(child, task)
            case "startEvent":
                event = StartEvent(attr['id'])
                new_elem = parse_flow_object(child, event)
            case "endEvent":
                event = EndEvent(attr['id'])
                new_elem = parse_flow_object(child, event)
            case "intermediateCatchEvent":
                event = IntermediateCatchEvent(attr['id'])
                new_elem = parse_flow_object(child, event)
            case "sequenceFlow":
                new_elem = SequenceFlow(attr['id'], attr['sourceRef'],
                                        attr['targetRef'], attr.get('name'))
            case "dataObjectReference":
                new_elem = DataObjectReference(attr['id'],
                                               attr['dataObjectRef'], attr.get('name'))
            case "dataStoreReference":
                new_elem = DataStoreReference(attr['id'],
                                              attr.get('dataStoreRef'), attr.get('name'))
            case "dataObject":
                new_elem = parse_data_object(child, process.id)
            case "dataStore":
                new_elem = parse_data_store(child)
            case "evidenceSource":
                new_elem = PotentialEvidenceSource(attr['id'], attr['attachedToRef'])
                add_pe_source(new_elem, elements)
            case "exclusiveGateway":
                gateway = ExclusiveGateway(attr['id'])
                new_elem = parse_flow_object(child, gateway)
            case "produces":
                association = Association(attr['id'], attr['sourceRef'], attr['targetRef'])
                attach_association(association, elements)
            case "evidenceAssociation":
                new_elem = EvidenceDataRelation(attr['id'], attr['sourceRef'], attr['targetRef'])

        store_element(new_elem, elements)


def store_element(new_elem: Element, elements: Dict[str, Element]):
    if new_elem is not None:
        key = new_elem.id
        elements[key] = new_elem


def parse(filename: str) -> Dict[str, Element]:
    elements = {}
    tree = ET.parse(filename)
    root = tree.getroot()

    for child in root:
        tag = get_tag(child)
        match tag:
            case 'process':
                parse_process(child, elements)
            case "collaboration":
                parse_collaboration(child, elements)

    return elements
