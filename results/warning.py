from results.response import BPMN4FRSSResponse


class BPMN4FRSSWarning(BPMN4FRSSResponse):
    def __init__(self, message=""):
        super().__init__(message)

