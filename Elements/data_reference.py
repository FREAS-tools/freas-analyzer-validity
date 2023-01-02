from elements.element import Element


class DataReference(Element):
    def __init__(self, elem_id, elem_type, data_ref, name=None):
        super().__init__(elem_id, elem_type, name)
        self.data_ref: str = data_ref   # artefact


class DataObjectReference(DataReference):
    def __init__(self, elem_id, elem_type, data_ref, name=None):
        super().__init__(elem_id, elem_type, data_ref, name)


class DataStoreReference(DataReference):
    def __init__(self, elem_id, elem_type, data_ref, name=None):
        super().__init__(elem_id, elem_type, data_ref, name)
