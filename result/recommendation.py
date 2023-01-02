from elements.artefact import Artefact
from elements.flow_object.flow_object import FlowObject


class Recommendation:
    def __init__(self, source, message):
        self.source: FlowObject | Artefact = source
        self.message: str = message
        # significance/improvement
