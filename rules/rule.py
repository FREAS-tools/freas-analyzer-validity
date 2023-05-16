from zope.interface import Interface
from typing import Dict, List, Optional

from elements.element import Element
from response.response import Response


class IRule(Interface):
    """
    Interface for rule objects that perform analysis on BPMN4FRSS models.
    """

    def evaluate(elements: Dict[str, Element], element_id: Optional[str]) -> Optional[Response]:
        """
        Evaluates the rule using the provided `elements` dictionary and optional `element_id` parameter.

        Parameters:
            elements (Dict[str, Element]): A dictionary of elements used in evaluating the rule.
            element_id (Optional[str]): An optional element ID used in the evidence quality analysis .

        Returns:
            Optional[Response]: A `Response` object if the rule is not satisfied,
            or `None` if the rule is satisfied.
        """
        pass

    def __create_response(solutions: List[str], message: str = '') -> Response:
        """
        Private helper method that creates a `Response` object.

        Parameters:
            solutions (List[str]): A list of elements IDs depending on the performed rule.
            message (str): A message providing the details of the performed rule.

        Returns:
            Response: A `Response` object.
        """
        pass
