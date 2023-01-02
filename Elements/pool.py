from elements.element import Element


# participant
class Pool(Element):
    def __init__(self, elem_id, elem_type, process_ref, name=None):
        super().__init__(elem_id, elem_type, name)
        self.process_ref: str = process_ref    # Process
