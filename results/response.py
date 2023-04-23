from typing import List


# make abstract
class Response:
    def __init__(self, message=""):
        self.source: List[str] = []
        self.message: str = message
