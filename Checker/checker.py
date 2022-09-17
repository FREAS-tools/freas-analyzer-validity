from z3 import *
from Parser.parser import parse

from Constrains.pe_check import check_pe
from Constrains.pes_check import check_pes
from Constrains.pet_check import check_pet
from Constrains.flow_check import check_flow


class Checker:
    def check(self, file_path: str):
        set_param(proof=True)

        elements = parse(file_path)
        s = Solver()
        s.set(unsat_core=True)

        s.push()
        flow_solver = check_flow(elements)
        s.add(flow_solver.assertions())
        # s.pop()
        #
        # s.push()
        # pe_solver = check_pe(elements)
        # s.add(pe_solver.assertions())
        # s.pop()
        #
        # s.push()
        # pes_solver = check_pes(elements)
        # s.add(pes_solver.assertions())
        # s.pop()
        #
        # s.push()
        # pet_solver = check_pet(elements)
        # s.add(pet_solver.assertions())
        # s.pop()

        # print(s.sexpr())

        if s.check() == sat:
            m = s.model()

            for dec in m.decls():
                print("%s = %s" % (dec.name(), m[dec]))
        else:
            # print(s.proof())
            print(s.check())
            # print(s.unsat_core())


checker = Checker()
checker.check("../Diagrams/recommendation.bpmn")
