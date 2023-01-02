from results.response import Response


class Recommendation(Response):
    def __init__(self, message=""):
        super().__init__(message)
        # significance/improvement

