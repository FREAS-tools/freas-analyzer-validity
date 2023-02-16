from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from parser.parser import parse
from rules.rule import IRule
from results.mistake import Mistake
from elements.element import Element
from results.response import Response
from results.severity import Severity
from elements.flow_object.task import Task
from elements.flow_object.hash_function import HashFunction
from elements.data_reference import DataObjectReference


# Checks if Hash Function output has Hash Proof type.
@implementer(IRule)
class HashProofType:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.severity = Severity.MEDIUM
        mistake.message = "Data Object that is the result of Hash Function needs to be of Hash Proof type"

        return mistake

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (task id, data object type)
        DataObject, mkDataObject, (first, second) = TupleSort("DataObject", [StringSort(), StringSort()])

        data_objects = []

        for _, value in elements.items():
            if isinstance(value, Task) and value.hash_fun is not None:
                data_ref: str = value.hash_fun.output  # Data Object Reference id
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: DataObject = elements.get(ref_obj.data)  # Data Object id

                data_obj_tuple = mkDataObject(StringVal(value.id), StringVal(type(data_obj).__name__))
                data_objects.append(data_obj_tuple)

        # data_objects += [mkDataObject(StringVal("bad"), StringVal("DataObject"))]

        # check if function output is HashProof
        def correct_type(data_object):
            return simplify(second(data_object)) == 'HashProof'

        def exists(data_object):
            return Or(
                [And(first(data_object) == first(obj), second(data_object) == second(obj)) for obj in data_objects])

        x = Consts('x', DataObject)
        s.add(Not(correct_type(x)))
        s.add(exists(x))

        solutions = []
        while s.check() == sat:
            model = s.model()
            # print(model)

            for dec in model.decls():
                print("%s = %s" % (dec.name(), model[dec]))
                s.add(dec() != model[dec])  # no duplicates
                solutions.append(simplify(first(model[dec])))  # only element's ID

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)

        return response


# elements = parse("../docs/diagrams/hash_correct.bpmn")
# fun = HashProofType()
# fun.evaluate(elements)
