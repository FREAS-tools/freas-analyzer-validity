import xml.etree.ElementTree as ET

from elements.artefact.data_object.data_object import DataObject
from elements.artefact.data_object.pot_evidence_type import PotentialEvidenceType
from elements.artefact.data_object.proof import HashProof, KeyedHashProof
from parser.parser import parse_data_object


def test_parse_data_object():
    # Test case for general Data Object
    elem_1 = ET.Element("dataObject")
    elem_1.attrib['id'] = "data_object_1"
    process_id = "process"

    data_object = parse_data_object(elem_1, process_id)

    assert isinstance(data_object, DataObject)
    assert data_object.id == "data_object_1"
    assert data_object.process_id == "process"

    # Test case for Potential Evidence Type
    elem_2 = ET.Element("dataObject")
    elem_2.attrib['id'] = "data_object_2"
    _ = ET.SubElement(elem_2, "potentialEvidenceType")

    data_object = parse_data_object(elem_2, process_id)

    assert isinstance(data_object, PotentialEvidenceType)
    assert data_object.id == "data_object_2"
    assert data_object.process_id == "process"

    # Test case for Hash Proof
    elem_3 = ET.Element("dataObject")
    elem_3.attrib['id'] = "data_object_3"
    _ = ET.SubElement(elem_3, "hash")

    data_object = parse_data_object(elem_3, process_id)

    assert isinstance(data_object, HashProof)
    assert data_object.id == "data_object_3"
    assert data_object.process_id == "process"

    # Test case for Keyed Hash
    elem_4 = ET.Element("dataObject")
    elem_4.attrib['id'] = "data_object_4"
    _ = ET.SubElement(elem_4, "keyedHash")

    data_object = parse_data_object(elem_4, process_id)

    assert isinstance(data_object, KeyedHashProof)
    assert data_object.id == "data_object_4"
    assert data_object.process_id == "process"
