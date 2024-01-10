from src.rules.semantic_hints.missing_pes import MissingPES


def test_av_parking_register_missing_pes(av_parking_register):
    rule = MissingPES()
    result = rule.evaluate(av_parking_register)

    data_objects_1 = ["DataObject_0ws7na4", "DataObject_1fqzgel"]
    data_objects_2 = ["DataObject_0hrcqay"]

    assert any(elem in result.source for elem in data_objects_1) and \
           any(elem in result.source for elem in data_objects_2)


def test_rics_issuing_permit_missing_pes(rics_issuing_permit_missing_pes):
    rule = MissingPES()
    result = rule.evaluate(rics_issuing_permit_missing_pes)

    data_objects = ["DataObject_0bpfd4d", "DataObject_1bufg17", "DataObject_16i36cz"]

    assert any(elem in result.source for elem in data_objects)
