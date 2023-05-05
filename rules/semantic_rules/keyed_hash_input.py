from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional
from elements.flow_object.tasks.task import Task
from parser.parser import parse
from results.severity import Severity
from rules.rule import IRule
from results.error import BPMN4FRSSError
from elements.element import Element
from results.response import BPMN4FRSSResponse as Response


# Check if Keyed Hash Function has exactly two inputs: one PotentialEvidence, and one key.
from rules.utils.semantic import add_mock_inputs


@implementer(IRule)
class KeyedHashFunInput:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        error = BPMN4FRSSError()
        error.source = solutions
        error.severity = Severity.MEDIUM
        error.message = "Task that executes the Keyed Hash Function must have exactly two inputs, " \
                        "one being a Potential Evidence Type, and a key."
        return error

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        # The sort, a constructor, and the accessors (task id, data object id, data object name, data object type)
        DataObjectSort, mkDataObject, (task_id, object_id, object_name, object_type) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort(), StringSort()])

        s = Solver()
        solutions = []

        for key, elem in elements.items():
            # check if element is a task, and if it has a hash function
            if not isinstance(elem, Task) or elem.hash_fun is None or elem.hash_fun.key is None:
                continue
            print("first for loop ", key)

            s.push()

            inputs = []  # contains all input data objects going to the current task
            for input_ in elem.data_input:
                data_ref_id = input_.source_ref
                data_ref = elements[data_ref_id]
                data = data_ref.data
                data_obj = elements[data]

                assert data_obj is not None

                inputs.append(mkDataObject(StringVal(key), StringVal(data_obj.id),
                                           StringVal(data_ref.name), StringVal(type(data_obj).__name__)))

            inputs = []
            if 0 <= len(inputs) < 2:
                inputs += add_mock_inputs(key, len(inputs), mkDataObject)

            def two_inputs():
                return len(inputs) == 2

            def correct_data_type(data_object):
                return simplify(object_type(data_object)) == 'PotentialEvidenceType'

            def correct_key_type(data_object):
                return simplify(object_name(data_object)) == 'key'

            def equal(data_object, key_object):
                return And(task_id(key_object) == task_id(data_object), object_id(key_object) == object_id(data_object),
                           object_type(key_object) == object_type(data_object))

            def exists(data_object):
                return Or([And(task_id(i) == task_id(data_object), object_id(i) == object_id(data_object),
                               object_name(i) == object_name(data_object), object_type(i) == object_type(data_object))
                           for i in inputs])

            input_one = Const('input_one', DataObjectSort)
            input_two = Const('input_two', DataObjectSort)

            correct_types = Or(And(correct_data_type(input_one), correct_key_type(input_two)),
                               And(correct_data_type(input_two), correct_key_type(input_one)))

            s.add(Or(Not(two_inputs()), Not(correct_types)))
            s.add(And(exists(input_one), exists(input_two)))
            s.add(Not(equal(input_one, input_two)))

            if s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    print("%s = %s" % (dec.name(), model[dec]))
                    s.add(dec() != model[dec])  # no duplicates
                    solutions.append(simplify(task_id(model[dec])))  # only element's ID
                    break

            # print(solutions)
            s.pop()

        return self.__create_response(solutions) if len(solutions) > 0 else None


# elements = parse("../../docs/diagrams/keyed_hash_correct.bpmn")
# fun = KeyedHashFunInput()
# fun.evaluate(elements)
