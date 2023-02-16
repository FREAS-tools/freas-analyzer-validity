from elements.element import Element


class DataReference(Element):
    def __init__(self, elem_id, data, name=None):
        super().__init__(elem_id, name)
        self.data: str = data   # artefact


class DataObjectReference(DataReference):
    def __init__(self, elem_id, data, name=None):
        super().__init__(elem_id, data, name)


class DataStoreReference(DataReference):
    def __init__(self, elem_id, data, name=None):
        super().__init__(elem_id, data, name)
