import xml.etree.ElementTree as ET

from parser.parser import get_tag


def test_get_tag():
    element_1 = ET.Element("{namespace}tag")
    tag = get_tag(element_1)
    assert tag == "tag"

    element_2 = ET.Element("tag")
    tag = get_tag(element_2)
    assert tag == "tag"
