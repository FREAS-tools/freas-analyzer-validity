import xml.etree.ElementTree as ET

from elements.pool import Pool
from elements.process import Process
from elements.element import Element
from elements.data_store import DataStore
from elements.flow_object.task import Task
from elements.flow_object.catch_event import *
from elements.flow_object.throw_event import *
from elements.flow.message_flow import MessageFlow
from elements.flow.sequence_flow import SequenceFlow
from elements.pe_source import PotentialEvidenceSource
from elements.flow_object.flow_object import FlowObject
from elements.evidence_data_relation import EvidenceDataRelation
from elements.hash_function import HashFunction, KeyedHashFunction
from elements.data_reference import DataObjectReference, DataStoreReference
from elements.data_object import DataObject, PotentialEvidenceType, DataHash
from elements.association import Association, DataInputAssociation, DataOutputAssociation

from typing import Dict


def get_tag(elem: ET.Element) -> str:  # without namespace
    return elem.tag.split('}')[1]


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
            case 'evidenceDataRelation':
                new_elem = parse_evidence_data_relation(child)

        if new_elem is not None:
            key = new_elem.id
            elements[key] = new_elem


def get_source_target_ref(elem: ET.Element):
    source, target = None, None

    for child in elem:
        tag = get_tag(child)
        if tag == "sourceRef":
            source = child.text
        if tag == "targetRef":
            target = child.text

    return source, target


def parse_evidence_data_relation(elem: ET.Element):
    source_ref, target_ref = get_source_target_ref(elem)
    edr = EvidenceDataRelation(elem.attrib['id'], source_ref, target_ref)

    return edr


def parse_flow_object(elem: ET.Element, obj: FlowObject) -> FlowObject:
    obj.name = elem.attrib.get('name')

    for child in elem:
        tag = get_tag(child)

        match tag:
            case "incoming":
                obj.incoming = child.text
            case "outgoing":
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
                obj.hash_fun = KeyedHashFunction(child.attrib.get('key'))

    return obj


def parse_data_object(elem: ET.Element) -> DataObject:
    for child in elem:
        tag = get_tag(child)
        if tag == "potentialEvidenceType":
            return PotentialEvidenceType(elem.attrib['id'])
        if tag == "hash":
            return DataHash(elem.attrib['id'])

    return DataObject(elem.attrib['id'])


def parse_data_store(elem: ET.Element) -> DataStore:
    data_store = DataStore(elem.attrib['id'])

    for child in elem:
        tag = get_tag(child)
        if tag == "storedPotentialEvidence":
            data_store.stored_pe.append(child.attrib['evidenceTypeRef'])

    return data_store


def parse_pe_source(elem: ET.Element) -> PotentialEvidenceSource:
    association = None

    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        if tag == "producesAssociation":
            association = Association(attr['sourceRef'], attr['targetRef'])
            break

    pes = PotentialEvidenceSource(elem.attrib['id'],
                                  elem.attrib['attachedToRef'], association)
    return pes


def add_pe_source(pe_source, elements: Dict[str, Element]):
    key = pe_source.attached_to_ref  # object id

    if elements.get(key) is not None:
        obj = elements[key]
        obj.pe_source = pe_source


def parse_process(elem: ET.Element, elements: Dict[str, Element]):
    process = Process(elem.attrib['id'])
    elements[process.id] = process

    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        new_elem = None

        match tag:
            case "startEvent":
                event = StartEvent(attr['id'])
                new_elem = parse_flow_object(child, event)
            case "task":
                task = Task(attr['id'])
                new_elem = parse_flow_object(child, task)
            case "endEvent":
                event = StartEvent(attr['id'])
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
                                              attr['dataStoreRef'], attr.get('name'))
            case "dataObject":
                new_elem = parse_data_object(child)
            case "dataStore":
                new_elem = parse_data_store(child)
            case "potentialEvidenceSource":
                new_elem = parse_pe_source(child)
                add_pe_source(new_elem, elements)

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


# elems = parse("../docs/diagrams/disputable_stored_in_same_context.bpmn")
# for k, v in elems.items():
#     print(k, "   ", v.name)

