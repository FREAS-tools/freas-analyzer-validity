from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from src.elements.artefact.data_object.data_object import DataObject
from src.elements.artefact.data_reference import DataObjectReference
from src.elements.flow_object.task.task import Task
from src.response.severity import Severity
from src.rules.rule import IRule
from src.response.error import Error
from src.elements.element import Element
from src.response.response import Response


@implementer(IRule)
class HashFunctionOutput:
    """
    Rule: Hash Function Output
    Description: This rule checks if Hash Function has exactly one output, being a Hash Proof.
    """

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = Error()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Task that executes the Hash Function must have exactly one output, " \
                        "Potential Evidence, being a Hash Proof."
        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (task id, data object id, data object type)
        data_object_sort, mk_data_object, (task_id, object_id, object_type) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort()])

        solutions = []

        # Goes through all tasks and checks their output data objects
        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.hash_fun is None or elem.pe_source is None:
                continue

            s.push()

            data_ref: str = elem.hash_fun.output
            ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
            data_obj: Optional[DataObject] = elements.get(ref_obj.data)

            assert data_obj is not None

            hash_output = mk_data_object(StringVal(key), StringVal(data_obj.id), StringVal(type(data_obj).__name__))

            # Data needed to check that task contains only one output
            outputs = []

            for output in elem.data_output:
                data_ref: str = output.target_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: Optional[DataObject] = elements.get(ref_obj.data)

                assert data_obj is not None

                outputs.append(mk_data_object(StringVal(key), StringVal(data_obj.id), StringVal(type(data_obj).__name__)))

            if len(outputs) == 0:
                outputs = [mk_data_object(StringVal(key), StringVal("None"), StringVal("None"))]

            # Compare hash function output data object (Hash Proof) id with the provided data object
            # also checks that the output is the same object as output of the hash function
            # then we know that both task output assoc and pes output assoc point to the same object
            def single_output(data_object):
                return And(task_id(hash_output) == task_id(data_object),
                           object_id(hash_output) == object_id(data_object),
                           object_type(hash_output) == object_type(data_object))

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'HashProof'

            # compare output objects with the provided data object
            def exists(data_object):
                return Or([And(task_id(o) == task_id(data_object), object_id(o) == object_id(data_object),
                               object_type(o) == object_type(data_object))
                           for o in outputs])

            x = Const('x', data_object_sort)

            # data object different from function output exists => multiple data outputs
            # or data object has different type then Hash Proof
            s.add(Or(Not(single_output(x)), Not(correct_type(x))))
            # s.add(Not(single_output(x)))

            # data object is contained in task output objects
            s.add(exists(x))

            # no need for while loop since we need the task not particular data objects
            if s.check() == sat:
                model = s.model()
                solutions.append(str(simplify(task_id(model[x]))).strip('"'))  # only element's ID

            s.pop()

        return self.__create_response(solutions) if len(solutions) > 0 else None
