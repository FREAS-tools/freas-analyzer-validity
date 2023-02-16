from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from elements.flow_object.task import Task
from parser.parser import parse
from rules.rule import IRule
from results.response import Response
from results.mistake import Mistake
from elements.element import Element


# Check if Keyed Hash Function has exactly two inputs: one PotentialEvidence, and one key.
@implementer(IRule)
class KeyedHashFunctionInput:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.message = "Task that executes the Keyed Hash Function can have exactly two inputs: " \
                          "one PotentialEvidence,and one key."
        return mistake

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (task id, data object id)
        DataObjSort, mkDataObjSort, (first, second) = TupleSort("DataObject", [StringSort(), StringSort()])
        solutions = []

        for key, value in elements.items():
            if not isinstance(value, Task) or value.hash_fun is None:
                continue

            s.push()
            inputs = []  # contains all input data objects going to the current task

            for input_obj in value.data_input:
                data_ref = input_obj.source_ref   # reference id to data object
                data = elements[data_ref].data    # data object id
                data_obj = elements[data]         # object
                inputs.append(mkDataObjSort(StringVal(key), StringVal(data_obj.id)))

            # if key == 'Activity_0l2nqgv':
            #     inputs.append(mkDataObjSort(StringVal('Activity_0l2nqgv'), StringVal('bad')))
            # else:
            #     inputs.append(mkDataObjSort(StringVal('MyTask'), StringVal('bad1')))

            input_ref = value.hash_fun.input     # reference to Keyed HF input data object
            input_id = elements[input_ref].data  # input object id
            input_obj = elements[input_id]       # input object

            key_ref = value.hash_fun.key         # reference to Keyed HF key data object
            key_id = elements[key_ref].data      # key object id
            key = elements[key_id]               # key object

            input_var = mkDataObjSort(StringVal(value.id), StringVal(input_obj.id))
            key_var = mkDataObjSort(StringVal(value.id), StringVal(key.id))

            # check if task has exactly two input data objects and that they are Keyed HF key and input
            def correct_input(var):
                return Or(second(var) == second(input_var), (second(var) == second(key_var)))

            # compares id from input objects to Keyed Hash Function input object and key object
            def exists(var):
                return Or([And(first(i) == first(var), second(i) == second(var)) for i in inputs])

            data_object = Consts('dataObject', DataObjSort)

            s.add(Not(correct_input(data_object)))
            s.add(exists(data_object))

            while s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    print("%s = %s" % (dec.name(), model[dec]))
                    s.add(dec() != model[dec])  # no duplicates
                    solutions.append(simplify(first(model[dec])))  # only element's ID

            s.pop()

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)

        return response


elements = parse("../docs/diagrams/keyed_hash_correct_I.bpmn")
fun = KeyedHashFunctionInput()
fun.evaluate(elements)
