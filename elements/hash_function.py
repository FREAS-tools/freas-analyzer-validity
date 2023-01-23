class HashFunction:
    def __init__(self, input_, output):
        self.input: str = input_  # DataObjectReference
        self.output: str = output  # DataObjectReference


class KeyedHashFunction(HashFunction):
    def __init__(self, key, input_=None, output=None):
        super().__init__(input_, output)
        self.key = key
