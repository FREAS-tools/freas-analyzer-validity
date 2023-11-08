from src.elements.element import Element


class FlowObject(Element):
    """
    Represents a BPMN4FRSS Flow Object.
    """
    def __init__(self, elem_id, name):
        """
        Constructor for FlowObject class.

        Parameters:
            elem_id (str): Element id
            name (str): Element name
        """
        super().__init__(elem_id, name)
