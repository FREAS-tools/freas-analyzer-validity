from typing import Optional


class HashFunction:
    """
    Represents a hash function.
    """
    def __init__(self, input_, output, key=None):
        """
        Constructor for HashFunction class.

        Parameters:
            input_ (str): Input Data Object id
            output (str): Output Data Object id
            key (str): Optional Key Data Object id
        """
        self.input: str = input_
        self.output: str = output
        self.key: Optional[str] = key
