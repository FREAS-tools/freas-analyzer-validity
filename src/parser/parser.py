from defusedxml.ElementTree import parse, fromstring
from xml.etree.ElementTree import Element as XmlElement

from typing import Dict
from types import MappingProxyType

from src.elements.element import Element
from src.elements.container.pool import Pool
from src.elements.container.process import Process
from src.elements.flow_object.task.task import Task
from src.elements.flow_object.activity import Activity
from src.elements.flow.message_flow import MessageFlow
from src.elements.flow.sequence_flow import SequenceFlow
from src.elements.flow_object.flow_object import FlowObject
from src.elements.flow_object.event.throw_event import EndEvent
from src.elements.artefact.data_store.data_store import DataStore
from src.elements.frss.evidence_data_store import EvidenceDataStore
from src.elements.artefact.data_object.data_object import DataObject
from src.elements.frss.evidence_data_relation import EvidenceDataRelation
from src.elements.flow_object.gateway.gateway import ExclusiveGateway, Gateway
from src.elements.frss.potential_evidence_source import PotentialEvidenceSource
from src.elements.frss.evidence_type.proof import HashProof, KeyedHashProof, Proof
from src.elements.artefact.data_reference import DataObjectReference, DataStoreReference
from src.elements.flow_object.event.catch_event import StartEvent, IntermediateCatchEvent
from src.elements.frss.evidence_type.potential_evidence_type import PotentialEvidenceType
from src.elements.flow.association import Association, DataInputAssociation, DataOutputAssociation
from src.elements.frss.forensic_ready_task.computations import AuthenticityComputation, DataTransformation, \
    HashFunction, IntegrityComputation


class Parser:
    """
    A class used to parse XML containing BPMN4FRSS model from a file or a string.

    Attributes:
        elements: A dictionary containing all parsed elements.

    """

    def __init__(self):
        self.elements = {}

    def parse_file(self, filename: str) -> Dict[str, Element]:
        """
        Parses the model XML from a file.
        """
        try:
            tree = parse(filename)
            root = tree.getroot()
            return self.__parse(root)
        except Exception as e:
            print(f"Error parsing file {filename}: {e}")
            return {}

    def parse_string(self, model_xml: str) -> Dict[str, Element]:
        """
        Parses the model XML from string.
        """
        root = fromstring(model_xml)
        return self.__parse(root)

    def __parse(self, root):
        for child in root:
            new_elem = None
            tag = self.__get_tag(child)

            match tag:
                case 'process':
                    new_elem = self.__parse_process(child)
                case "collaboration":
                    self.__parse_collaboration(child)
                case "dataStore":
                    new_elem = self.__parse_data_store(child)

            self.__store_element(new_elem)

        return MappingProxyType(self.elements)  # immutable dict

    def __parse_process(self, elem: XmlElement) -> Process:
        process = Process(elem.attrib['id'])

        for child in elem:
            tag = self.__get_tag(child)
            attr = child.attrib
            new_elem = None

            match tag:
                case "task" | "startEvent" | "endEvent" | "intermediateCatchEvent" | "exclusiveGateway" | "subProcess":
                    new_elem = self.__parse_flow_object(tag, child)
                case "sequenceFlow":
                    new_elem = SequenceFlow(attr['id'], attr['sourceRef'],
                                            attr['targetRef'], attr.get('name'))
                case "dataObjectReference":
                    new_elem = DataObjectReference(attr['id'],
                                                   attr['dataObjectRef'], self.__get_name(child))
                case "dataStoreReference":
                    new_elem = DataStoreReference(attr['id'],
                                                  attr.get('dataStoreRef'), process.id, self.__get_name(child))
                case "dataObject":
                    new_elem = self.__parse_data_object(child, process.id)
                case "evidenceSource":
                    new_elem = PotentialEvidenceSource(attr['id'], attr['attachedToRef'])
                    self.__add_pe_source(new_elem)
                case "produces":
                    association = Association(attr['id'], attr['sourceRef'], attr['targetRef'])
                    self.__attach_association(association)
                case "evidenceAssociation":
                    new_elem = EvidenceDataRelation(attr['id'], attr['sourceRef'], attr['targetRef'])

            self.__store_element(new_elem)

        return process

    def __parse_collaboration(self, elem: XmlElement):
        for child in elem:
            tag = self.__get_tag(child)
            attr = child.attrib
            new_elem = None

            match tag:
                case 'participant':
                    # Collapsed processes do not have 'processRef'
                    # Store only the non-collapsed ones
                    if 'processRef' in attr:
                        new_elem = Pool(attr['id'], attr['processRef'], attr.get('name'))
                    else:
                        new_elem = Pool(attr['id'], None, attr.get('name'))
                case 'messageFlow':
                    new_elem = MessageFlow(attr['id'], attr['sourceRef'],
                                           attr['targetRef'], attr.get('name'))

            self.__store_element(new_elem)

    def __parse_flow_object(self, tag: str, elem: XmlElement) -> FlowObject:
        attr = elem.attrib
        flow_object = None

        match tag:
            case "task" | "subProcess":
                flow_object = Task(attr['id'], attr.get('name'))
                self.__parse_activity(flow_object, elem)
            case "startEvent":
                flow_object = StartEvent(attr['id'], attr.get('name'))
                self.__parse_activity(flow_object, elem)
            case "endEvent":
                flow_object = EndEvent(attr['id'], attr.get('name'))
                self.__parse_activity(flow_object, elem)
            case "intermediateCatchEvent":
                flow_object = IntermediateCatchEvent(attr['id'], attr.get('name'))
                self.__parse_activity(flow_object, elem)
            case "exclusiveGateway":
                flow_object = ExclusiveGateway(attr['id'], attr.get('name'))
                self.__parse_gateway(flow_object, elem)

        flow_object.name = attr.get('name') if flow_object else None

        return flow_object

    def __parse_activity(self, activity: Activity, elem: XmlElement):
        for child in elem:
            tag = self.__get_tag(child)

            match tag:
                case "incoming":
                    activity.incoming = child.text
                case "outgoing":
                    activity.outgoing = child.text
                case "dataOutputAssociation":
                    _, target = self.__get_source_target_ref(child)
                    association = DataOutputAssociation(child.attrib['id'], activity.id, target)
                    activity.data_output.append(association)
                case "dataInputAssociation":
                    source, _ = self.__get_source_target_ref(child)
                    association = DataInputAssociation(child.attrib['id'], source, activity.id)
                    activity.data_input.append(association)
                # Task specific functions
                case "authenticityComputation":
                    activity.computation = AuthenticityComputation(child.attrib.get('input'),
                                                                   child.attrib.get('output'))
                case "integrityComputation":
                    activity.computation = IntegrityComputation(child.attrib.get('input'), child.attrib.get('output'))
                case "dataTransformation":
                    activity.computation = DataTransformation(child.attrib.get('input'), child.attrib.get('output'))
                case "hashFunction":
                    activity.computation = HashFunction(child.attrib.get('input'), child.attrib.get('output'))
                case "keyedHashFunction":
                    activity.computation = HashFunction(child.attrib.get('input'), child.attrib.get('output'),
                                                        child.attrib.get('key'))
        return

    def __parse_gateway(self, gateway: Gateway, elem: XmlElement):
        for child in elem:
            tag = self.__get_tag(child)

            match tag:
                case "incoming":
                    gateway.incoming.append(child.text)
                case "outgoing":
                    gateway.outgoing.append(child.text)
        return

    def __parse_data_object(self, elem: XmlElement, process_id: str) -> DataObject:
        for child in elem:
            tag = self.__get_tag(child)
            if tag == "potentialEvidence":
                return self.__parse_evidence_type(child, elem.attrib['id'], process_id)

        return DataObject(elem.attrib['id'], process_id)

    def __parse_evidence_type(self, elem: XmlElement, elem_id: str, process_id: str) -> PotentialEvidenceType:
        for child in elem:
            tag = self.__get_tag(child)
            if tag == "proof":
                return Proof(elem_id, process_id)
            if tag == "hashProof":
                return HashProof(elem_id, process_id)
            if tag == "keyedHashProof":
                return KeyedHashProof(elem_id, process_id)

        return PotentialEvidenceType(elem_id, process_id)

    def __parse_data_store(self, elem: XmlElement) -> DataStore:
        for child in elem:
            tag = self.__get_tag(child)
            if tag == "evidenceStore":
                ev_data_store = EvidenceDataStore(elem.attrib['id'])
                for sub_child in child:
                    subtag = self.__get_tag(sub_child)
                    if subtag == "stores":
                        ev_data_store.stored_pe.append(sub_child.text)
                return ev_data_store

        return DataStore(elem.attrib['id'])

    def __add_pe_source(self, pe_source: PotentialEvidenceSource):
        key = pe_source.attached_to_ref  # object id
        elem = self.elements.get(key)

        if elem is not None:
            elem.pe_source = pe_source

    def __attach_association(self, association: Association):
        pe_source_id = association.source_ref
        pe_source = self.elements.get(pe_source_id)
        
        if pe_source is not None:
            pe_source.association = association

    def __get_source_target_ref(self, elem: XmlElement):
        source, target = None, None

        for child in elem:
            tag = self.__get_tag(child)
            if tag == "sourceRef":
                source = child.text
            if tag == "targetRef":
                target = child.text

        return source, target

    def __store_element(self, new_elem: Element):
        if new_elem is not None:
            key = new_elem.id
            self.elements[key] = new_elem

    @staticmethod
    def __get_tag(elem: XmlElement) -> str:  # without namespace
        tag_list = elem.tag.split('}')

        if len(tag_list) > 1:
            return tag_list[1]
        return tag_list[0]


    @staticmethod
    def __get_name(elem: XmlElement) -> str:
        name = elem.attrib.get('name')
        
        return name.replace("\n", " ") if name else None