from typing import List

from results.mistake import Mistake
from results.recommendation import Recommendation
from results.response import Response


class Result:
    def __init__(self):
        self.mistakes: List[Mistake] = []
        self.recommendations: List[Recommendation] = []
        self.evidence_stores: List[Response] = []
