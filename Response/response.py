from typing import List

from Response.mistake import Mistake
from Response.recommendation import Recommendation


class Response:
    def __init__(self):
        self.num_of_mistakes: int = 0
        self.num_of_rec: int = 0
        self.mistakes: List[Mistake] = []
        self.recommendations: List[Recommendation] = []


