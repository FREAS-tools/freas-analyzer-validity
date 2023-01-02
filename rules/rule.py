from zope.interface import Interface
from typing import Dict, Optional, List

from elements.element import Element
from results.response import Response


class IRule(Interface):
    """Add doc"""

    def evaluate(elements: Dict[str, Element]) -> Optional[Response]:
        pass

    def __create_response(solutions: List[str]) -> Response:
        pass
