from z3 import *
from zope.interface import implementer
from typing import Dict, List, Optional

from elements.flow_object.task import Task
from parser.parser import parse
from rules.rule import IRule
from results.response import Response
from results.mistake import Mistake
from elements.element import Element


# Check if Hash Function has exactly one output, referring to a Potential Evidence, being a Hash Proof.
# assumes that task has PES that produces Hash Proof
@implementer(IRule)
class HashFunctionOutput:

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        mistake = Mistake()
        mistake.source = solutions
        mistake.message = "Task that executes the (Keyed) Hash Function can have exactly one output, " \
                          "PotentialEvidence, being a (Keyed) Hash Proof."
        return mistake

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:
        s = Solver()

        # The sort, a constructor, and the accessors (task id, data object id)
        DataObjSort, mkDataObjSort, (first, second) = TupleSort("DataObject", [StringSort(), StringSort()])
        solutions = []

        for key, value in elements.items():
            if not isinstance(value, Task) or value.hash_fun is None or value.pe_source is None:
                continue

            s.push()
            outputs = []  # contains all output data objects emerging from the current task

            for output in value.data_output:
                data_ref = output.target_ref    # reference to data object
                data = elements[data_ref].data  # id
                data_obj = elements[data]       # object
                outputs.append(mkDataObjSort(StringVal(key), StringVal(data_obj.id)))

            # if key == 'Activity_0l2nqgv':
            #     outputs.append(mkDataObjSort(StringVal('Activity_0l2nqgv'), StringVal('bad')))
            # else:
            #     outputs.append(mkDataObjSort(StringVal('MyTask'), StringVal('bad1')))

            data_ref = value.pe_source.association.target_ref  # reference to data object being a hash proof
            data = elements[data_ref].data                     # data object id
            hash_proof = elements[data]                        # object
            proof_var = mkDataObjSort(StringVal(key), StringVal(hash_proof.id))

            # compare hash function output data object (Hash Proof) id with the provided data object
            def correct_object(data_object):
                return second(proof_var) == second(data_object)

            # compare output object with the provided data object
            def exists(data_object):
                return Or([And(first(o) == first(data_object), second(o) == second(data_object)) for o in outputs])

            x = Consts('x', DataObjSort)

            # data object different from function output exists
            s.add(Not(correct_object(x)))
            # data object is contained in task output objects
            s.add(exists(x))

            while s.check() == sat:
                model = s.model()

                for dec in model.decls():
                    # print("%s = %s" % (dec.name(), model[dec]))
                    s.add(dec() != model[dec])  # no duplicates
                    solutions.append(simplify(first(model[dec])))  # only element's ID

            s.pop()

        if len(solutions) == 0:
            return None

        response = self.__create_response(solutions)

        return response


# elements = parse("../docs/diagrams/hash_correct_I.bpmn")
# fun = HashFunctionOutput()
# fun.evaluate(elements)
