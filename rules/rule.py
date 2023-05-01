from zope.interface import Interface
from typing import Dict, List, Optional

from elements.element import Element
from results.response import BPMN4FRSSResponse


class IRule(Interface):
    """Add doc"""

    def evaluate(elements: Dict[str, Element]) -> Optional[BPMN4FRSSResponse]:
        pass

    def __create_response(solutions: List[str], message: str = '') -> BPMN4FRSSResponse:
        pass
