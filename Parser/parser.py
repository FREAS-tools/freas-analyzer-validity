import xml.etree.ElementTree as ET

from Elements.Pool.pool import Pool
from Elements.Pool.process import Process
from Elements.FlowObject.task import Task
from Elements.Artefact.data_object import *
from Elements.Element.element import Element
from Elements.FlowObject.catch_event import *
from Elements.FlowObject.throw_event import *
from Elements.Flow.message_flow import MessageFlow
from Elements.Flow.sequence_flow import SequenceFlow
from Elements.FlowObject.flow_object import FlowObject
from Elements.Association.association import Association
from Elements.PESource.pe_source import PotentialEvidenceSource
from Elements.DataReference.data_reference import DataObjectReference
from Elements.EvidenceDataRelation.evidence_data_relation import EvidenceDataRelation

from typing import Dict, Union


def get_tag(elem: ET.Element) -> str:  # without namespace
    return elem.tag.split('}')[1]


def parse_collaboration(elem: ET.Element, elements: Dict[str, Element]):
    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        new_elem = None

        match tag:
            case 'participant':
                new_elem = Pool(attr['id'], Pool, attr['processRef'], attr.get('name'))
            case 'messageFlow':
                new_elem = MessageFlow(attr['id'], MessageFlow, attr['sourceRef'],
                                       attr['targetRef'], attr.get('name'))
            case 'evidenceDataRelation':
                new_elem = parse_evidence_dr(child)

        if new_elem is not None:
            key = new_elem.id
            elements[key] = new_elem


def parse_evidence_dr(elem: ET.Element):
    source_ref = None
    target_ref = None

    for child in elem:
        tag = get_tag(child)
        if tag == "sourceRef":
            source_ref = child.text
        if tag == "targetRef":
            target_ref = child.text

    edr = EvidenceDataRelation(elem.attrib['id'], EvidenceDataRelation, source_ref, target_ref)
    return edr


def parse_flow_object(elem: ET.Element, obj: FlowObject) -> FlowObject:
    obj.name = elem.attrib.get('name')

    for child in elem:
        tag = get_tag(child)
        if tag == "incoming":
            obj.incoming = child.text
        if tag == "outgoing":
            obj.outgoing = child.text
    return obj


def parse_data_object(elem: ET.Element) -> DataObject:
    for child in elem:
        tag = get_tag(child)
        if tag == "potentialEvidenceType":
            return PotentialEvidenceType(elem.attrib['id'], PotentialEvidenceType)
    return DataObject(elem.attrib['id'], DataObject)


def parse_pe_source(elem: ET.Element) -> PotentialEvidenceSource:
    association = None

    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        if tag == "producesAssociation":
            association = Association(attr['sourceRef'], attr['targetRef'])
            break

    pes = PotentialEvidenceSource(elem.attrib['id'], PotentialEvidenceSource,
                                  elem.attrib['attachedToRef'], association)
    return pes


def add_pe_source(pe_source, elements: Dict[str, Element]):
    key = pe_source.attached_to_ref  # object id

    if elements.get(key) is not None:
        obj = elements[key]
        obj.pe_source = pe_source


def parse_process(elem: ET.Element, elements: Dict[str, Element]):
    proc = Process(elem.attrib['id'], Process)
    elements[proc.id] = proc

    for child in elem:
        tag = get_tag(child)
        attr = child.attrib
        new_elem = None

        match tag:
            case "startEvent":
                event = StartEvent(attr['id'], StartEvent)
                new_elem = parse_flow_object(child, event)
            case "task":
                task = Task(attr['id'], Task)
                new_elem = parse_flow_object(child, task)
            case "endEvent":
                event = StartEvent(attr['id'], EndEvent)
                new_elem = parse_flow_object(child, event)
            case "intermediateCatchEvent":
                event = IntermediateCatchEvent(attr['id'], IntermediateCatchEvent)
                new_elem = parse_flow_object(child, event)
            case "sequenceFlow":
                new_elem = SequenceFlow(attr['id'], SequenceFlow, attr['sourceRef'],
                                        attr['targetRef'], attr.get('name'))
            case "dataObjectReference":
                new_elem = DataObjectReference(attr['id'], DataObjectReference,
                                               attr['dataObjectRef'], attr.get('name'))
            case "dataObject":
                new_elem = parse_data_object(child)
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
