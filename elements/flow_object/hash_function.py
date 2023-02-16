from typing import Optional


class HashFunction:
    def __init__(self, input_, output, key=None):
        self.input: str = input_        # DataObjectReference
        self.output: str = output       # DataObjectReference
        self.key: Optional[str] = key   # DataObjectReference
