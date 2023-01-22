from elements.element import Element


# participant
class Pool(Element):
    def __init__(self, elem_id, process_ref, name=None):
        super().__init__(elem_id, name)
        self.process_ref: str = process_ref    # Process
