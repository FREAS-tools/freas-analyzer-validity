from src.rules.semantic_hints.message_flow_pes import MessageFlowPES


def test_message_flow_pes(missing_message_flow_pes_elements):
    rule = MessageFlowPES()
    result = rule.evaluate(missing_message_flow_pes_elements)

    expected_flow_objects = ["Task_02p51vl", "IntermediateThrowEvent_0647pg8"]

    for elem in result.source:
        assert elem in expected_flow_objects
