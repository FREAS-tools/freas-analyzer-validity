from typing import List

from results.mistake import Mistake
from results.recommendation import Recommendation


class Result:
    def __init__(self):
        self.num_of_mistakes: int = 0
        self.num_of_recommendations: int = 0
        self.mistakes: List[Mistake] = []
        self.recommendations: List[Recommendation] = []
