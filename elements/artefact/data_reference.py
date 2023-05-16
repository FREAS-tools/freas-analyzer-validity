from elements.element import Element


class DataReference(Element):
    """
    Represents a BPMN4FRSS Data Reference.
    """
    def __init__(self, elem_id, data, name=None):
        """
        Constructor for DataReference class.

        Parameters:
            elem_id (str): Element id
            data (str): id of the Data Object or Data Store
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, name)
        self.data: str = data


class DataObjectReference(DataReference):
    """
    Represents a BPMN4FRSS Data Object Reference.
    """
    def __init__(self, elem_id, data, name=None):
        """
        Constructor for DataObjectReference class.

        Parameters:
            elem_id (str): Element id
            data (str): id of the Data Object
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, data, name)


class DataStoreReference(DataReference):
    """
    Represents a BPMN4FRSS Data Store Reference.
    """
    def __init__(self, elem_id, data, name=None):
        """
        Constructor for DataStoreReference class.

        Parameters:
            elem_id (str): Element id
            data (str): id of the Data Store
            name (Optional[str]): Element name
        """
        super().__init__(elem_id, data, name)
