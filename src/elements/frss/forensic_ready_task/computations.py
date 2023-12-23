from typing import Optional


class Computation:
    """
    Represents a general task computation.
    """
    def __init__(self, input_, output):
        """
        Constructor for Computation class.

        Parameters:
            input_ (str): Data Input Association id
            output (str): Data Output Association id
        """
        self.input: str = input_
        self.output: str = output


class IntegrityComputation(Computation):
    """
    Represents a task computation that verifies integrity.
    """
    def __init__(self, input_, output):
        """
        Constructor for IntegrityComputation class.

        Parameters:
            input_ (str): Data Input Association id
            output (str): Data Output Association id
        """
        super().__init__(input_, output)


class AuthenticityComputation(Computation):
    """
    Represents a task function that verifies authenticity.
    """
    def __init__(self, input_, output):
        """
        Constructor for AuthenticityComputation class.

        Parameters:
            input_ (str): Data Input Association id
            output (str): Data Output Association id
        """
        super().__init__(input_, output)



class DataTransformation(Computation):
    """
    Represents a task function that executes data transformation.
    """
    def __init__(self, input_, output):
        """
        Constructor for DataTransformation class.

        Parameters:
            input_ (str): Data Input Association id
            output (str): Data Output Association id
        """
        super().__init__(input_, output)


class HashFunction(IntegrityComputation):
    """
    Represents a task hashing function.
    """
    def __init__(self, input_, output, key=None):
        """
        Constructor for HashFunction class.

        Parameters:
            input_ (str): Data Input Association id
            output (str): Data Output Association id
            key (str): Optional Key Data Object id
        """
        super().__init__(input_, output)
        self.key: Optional[str] = key
