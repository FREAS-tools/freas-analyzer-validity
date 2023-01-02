from elements.artefact import Artefact
from elements.flow_object.flow_object import FlowObject
from result.severity import Severity


class Mistake:
    def __init__(self, source, message, severity):
        self.source: FlowObject | Artefact = source
        self.message: str = message
        self.severity: Severity = severity
