class Element:
    def __init__(self, elem_id, elem_type, name=None):
        self.id = elem_id
        self.type = elem_type
        self.name: str = "" if name is None else name

