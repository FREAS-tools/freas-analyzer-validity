class Element:
    def __init__(self, elem_id, name=None):
        self.id = elem_id
        self.name: str = "" if name is None else name

