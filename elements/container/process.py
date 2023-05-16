from elements.element import Element


class Process(Element):
    """
    Represents a BPMN4FRSS Process.
    """
    def __init__(self, elem_id):
        """
        Constructor for Process class.

        Parameters:
            elem_id (str): Element id
        """
        super().__init__(elem_id)
