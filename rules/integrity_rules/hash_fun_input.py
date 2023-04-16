from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from elements.data_object import DataObject
from parser.parser import parse
from rules.rule import IRule
from results.mistake import Mistake
from elements.element import Element
from results.response import Response
from results.severity import Severity
from elements.flow_object.tasks.task import Task
from elements.data_reference import DataObjectReference


# Check if Hash Function has input of Potential Evidence Type
# Check that hash fun has only one input and that it has PE Type
@implementer(IRule)
class HashFunctionInput:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.severity = Severity.MEDIUM
        mistake.message = "Task that executes the Hash Function must have exactly one input, " \
                          "being a Potential Evidence Type."

        return mistake

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (task id, data object id, data object type)
        DataObjectSort, mkDataObject, (task_id, object_id, object_type) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort()])

        solutions = []

        # goes through all tasks and checks their output data objects
        for key, elem in elements.items():
            if not isinstance(elem, Task) or elem.hash_fun is None:
                continue

            s.push()

            data_ref: str = elem.hash_fun.input
            ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
            data_obj: Optional[DataObject] = elements.get(ref_obj.data)

            assert data_obj is not None

            hash_input = mkDataObject(StringVal(key), StringVal(data_obj.id), StringVal(type(data_obj).__name__))

            # data needed to check that task contains only one input
            inputs = []  # contains all input data objects to the current task

            for input_ in elem.data_input:
                data_ref: str = input_.source_ref
                ref_obj: Optional[DataObjectReference] = elements.get(data_ref)
                data_obj: Optional[DataObject] = elements.get(ref_obj.data)

                assert data_obj is not None

                inputs.append(mkDataObject(StringVal(key), StringVal(data_obj.id), StringVal(type(data_obj).__name__)))

            # inputs = []
            if len(inputs) == 0:
                inputs = [mkDataObject(StringVal(key), StringVal("None"), StringVal("None"))]

            # if key == 'Activity_0l2nqgv':
            #     inputs.append(mkDataObject(StringVal('Activity_0l2nqgv'), StringVal('bad'),
            #                                StringVal("PotentialEvidenceType")))
            #     # inputs = [mkDataObject(StringVal('Activity_0l2nqgv'), StringVal('bad'), StringVal("DataObject"))]
            # else:
            #     inputs.append(mkDataObject(StringVal('MyTask'), StringVal('bad1'), StringVal("HashProof")))

            def single_input(data_object):
                return And(task_id(hash_input) == task_id(data_object),
                           object_id(hash_input) == object_id(data_object),
                           object_type(hash_input) == object_type(data_object))

            def correct_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def exists(data_object):
                return Or([And(task_id(o) == task_id(data_object), object_id(o) == object_id(data_object),
                               object_type(o) == object_type(data_object))
                           for o in inputs])

            x = Const('x', DataObjectSort)

            # data object different from function output exists => multiple data inputs
            # or data object has different type then PotentialEvidenceType
            s.add(Or(Not(single_input(x)), Not(correct_type(x))))

            # data object is contained in task output objects
            s.add(exists(x))

            # no need for while loop since we need the task not particular data objects
            if s.check() == sat:
                model = s.model()
                print(model)
                solutions.append(simplify(task_id(model[x])))  # only element's ID

            s.pop()

        return self.__create_response(solutions) if len(solutions) > 0 else None


# fun = HashFunctionInput()
# print('1. ')
# elements = parse("../../docs/diagrams/hash_correct.bpmn")
# fun.evaluate(elements)
# print('2. ')
# elements = parse("../../docs/diagrams/keyed_hash_correct.bpmn")
# fun.evaluate(elements)

