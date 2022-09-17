from z3 import *
# Declared Z3 sorts based on the classes of elements


TaskSort = DeclareSort("TaskSort")
EventSort = DeclareSort("EventSort")
FlowObjSort = DeclareSort("FlowObjSort")
PESourceSort = DeclareSort("PESourceSort")
AssociationSort = DeclareSort("AssociationSort")
MessFlowSort = DeclareSort("MessFlowSort")
ArtefactSort = DeclareSort("ArtefactSort")
PETSort = DeclareSort("PETSort")  # PotentialEvidenceType
DataObjectSort = DeclareSort("DataObjectSort")
