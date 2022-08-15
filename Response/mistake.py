from Elements.Artefact.artefact import Artefact
from Elements.FlowObject.flow_object import FlowObject
from Response.severity import Severity


class Mistake:
    def __init__(self, source, message, severity):
        self.source: FlowObject | Artefact = source
        self.message: str = message
        self.severity: Severity = severity
