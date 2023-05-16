from typing import List, Dict, Optional

from z3 import *
from zope.interface import implementer

from elements.artefact.data_object.data_object import DataObject
from elements.element import Element
from elements.flow_object.task.task import Task
from response.response import Response
from response.warning import Warning
from rules.rule import IRule
from rules.utils.semantic import get_participant


@implementer(IRule)
class SameEvidenceStore:
    """
    Rule:
    Description: This rule check that the Hash Proof is stored independently of Potential Evidence,
    i.e., in a different Evidence Context.
    """

    @staticmethod
    def __create_response(solutions: List[str]) -> Response:
        warning = Warning()
        warning.source = solutions
        warning.message = "The HashProof MUST be stored independently of PotentialEvidence," \
                          " different EvidenceContext."

        return warning

    def evaluate(self, elements: Dict[str, Element]) -> Optional[Response]:

        # FORMALIZATION
        # Define the Z3 tuple sort representing data object, containing the following fields:
        # participant ID, data object id, and data object name
        DataObjectSort, mkDataObject, (participant_id, object_id, object_name) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort()])

        # TaskSort, mkTask, (participant_id, task_id, input_name, output_name) = \
        #     TupleSort("DataObject", [StringSort(), StringSort(), StringSort(), StringSort()])

        solutions = []
        for key, elem in elements.items():
            # Find all tasks that execute a hash function
            if not isinstance(elem, Task) or elem.hash_fun is None:
                continue

            # Find the input and output data objects of the hash function
            # and create a Z3 DataObject representing them
            input_ref = elements[elem.hash_fun.input]
            fun_input = elements[input_ref.data]
            participant = get_participant(elements, fun_input.process_id)

            z3_fun_input = mkDataObject(StringVal(participant), StringVal(fun_input.id), StringVal(input_ref.name))
            # z3_fun_input = mkDataObject(StringVal("id_1"), StringVal("obj_id_1"), StringVal("Evidence"))

            output_ref = elements[elem.hash_fun.output]
            fun_output = elements[output_ref.data]
            participant = get_participant(elements, fun_output.process_id)

            z3_fun_output = mkDataObject(StringVal(participant), StringVal(fun_output.id), StringVal(output_ref.name))
            # z3_fun_output = mkDataObject(StringVal("id_1"), StringVal("obj_id_2"), StringVal("Proof"))

            # Get all data objects in the model and create Z3 DataObject representing them
            z3_data_objects = []
            for value in elements.values():
                if not isinstance(value, DataObject):
                    continue

                participant = get_participant(elements, value.process_id)
                z3_data_objects.append(mkDataObject(StringVal(participant), StringVal(value.id), StringVal(value.name)))

            z3_data_objects = [mkDataObject(StringVal("id_1"), StringVal("key_id_1"), StringVal("Proof")),
                               mkDataObject(StringVal("id_2"), StringVal("key_id_2"), StringVal("key_name_1")),
                               mkDataObject(StringVal("id_1"), StringVal("key_id_3"), StringVal("Evidence")),

                               mkDataObject(StringVal("id_1"), StringVal("obj_id_2"), StringVal("Proof")),
                               mkDataObject(StringVal("id_1"), StringVal("obj_id_1"), StringVal("Evidence"))]

            # da li postoji do koji ima isto ime a razliciti paricipant za isptuti  ili za output
            # MZD ODDATI DA PARTICIpat inputa != partic outputa
            # CONSTRAINTS

            def exists(data_object):
                return Or([data_object == obj for obj in z3_data_objects])

            s = Solver()
            proof = Const('proof', DataObjectSort)
            pot_evidence = Const('pot_evidence', DataObjectSort)

            def stored():
                return Not(Or(
                    [And(object_name(z3_fun_input) == object_name(k),
                         participant_id(z3_fun_input) != participant_id(k))
                     for k in z3_data_objects]
                ))

            # s.add(Not(Or(
            #     [And(input_name(task) == object_name(obj), participant_id(task) != participant_id(obj)) for obj in
            #      z3_data_objects])))
            # s.add(Not(Or(
            #     [And(output_name(task) == object_name(obj), participant_id(task) != participant_id(obj)) for obj in
            #      z3_data_objects])))

            # s.add(stored())
            s.add(And(exists(proof), exists(pot_evidence)))

            # s.add(object_name(pot_evidence) == object_name(z3_fun_input))
            # proof same name different participant
            # proof name == output name

            # # proof stored in different participant
            # proof_stored = And(Distinct(participant_id(proof), participant_id(z3_fun_output)),  # same participant
            #                    Not(Distinct(object_name(proof), object_name(z3_fun_output))))  # same name

            # # potential evidence stored in different participant
            # pot_evidence_stored = And(Distinct(participant_id(pot_evidence), participant_id(z3_fun_input)),
            #                           Not(Distinct(object_name(pot_evidence), object_name(z3_fun_input))))
            # s.add(Not(Or(proof_stored, pot_evidence_stored)))
            # s.add(Or(proof_stored, pot_evidence_stored))
            # s.add(Or(Not(proof_stored), Not(pot_evidence_stored)))

            # trazimo data object koji nema u nekom drugom participantu isto ime
            # sto bi znacilo da svi data objecti moraju ili da budu u isto participantu ili da imaju razlicito ime
            def stored2(obj):
                return And(
                    [Or(participant_id(obj) == participant_id(k), object_name(obj) != object_name(k))
                     for k in z3_data_objects]
                )

            def stored3(obj):
                return And(
                    [If(object_name(obj) == object_name(k), participant_id(obj) == participant_id(k), True)
                     for k in z3_data_objects]
                )

            # s.add(And(exists(proof)))
            # s.add(Or(proof == z3_fun_input, proof == z3_fun_output))
            s.add(proof == z3_fun_output)
            s.add(pot_evidence == z3_fun_input)
            # s.add(And(object_name(pot_evidence) == object_name(z3_fun_input),
            #           participant_id(pot_evidence) == participant_id(z3_fun_input)))
            #
            # s.add(And(object_name(proof) == object_name(z3_fun_output),
            #           participant_id(proof) == participant_id(z3_fun_output)))

            # s.add(participant_id(proof) != participant_id(z3_fun_input))
            s.add(stored2(proof))
            s.add(stored2(pot_evidence))

            # MODEL
            while s.check() == sat:
                model = s.model()
                # print(model)
                # model[task]
                for dec in model.decls():  # izbaci
                    # proveri da je task
                    print("%s = %s" % (dec.name(), model[dec]))
                    s.add(dec() != model[dec])  # izbaci
                    solutions.append(simplify(object_id(model[dec])))  # only element's ID

        # print(solutions)
        return self.__create_response(solutions) if len(solutions) > 0 else None

# elements = parse("../../documentation/diagrams/keyed_hash_correct.bpmn")
# fun = SameEvidenceStore()
# fun.evaluate(elements)
