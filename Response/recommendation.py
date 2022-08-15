from Elements.Artefact.artefact import Artefact
from Elements.FlowObject.flow_object import FlowObject


class Recommendation:
    def __init__(self, source, message):
        self.source: FlowObject | Artefact = source
        self.message: str = message
        # significance/improvement
