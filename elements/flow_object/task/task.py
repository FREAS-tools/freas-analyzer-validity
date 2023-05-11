from typing import Optional

from elements.flow_object.activity import Activity
from elements.flow_object.hash_function import HashFunction


class Task(Activity):
    def __init__(self, elem_id, name=None, incoming=None, outgoing=None, pe_source=None):
        super().__init__(elem_id, name, incoming, outgoing, pe_source)
        self.hash_fun: Optional[HashFunction] = None
