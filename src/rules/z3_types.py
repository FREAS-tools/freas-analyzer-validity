from z3 import *

# NOTE:  The accessor's names must not be repeated. Otherwise, the last one defined will be used.

# Define the Z3 tuple sort representing data store, containing the following fields:
# data store ID, array of stored potential evidence and their number
data_store_sort, mk_data_store, (store_id, stored_pe, pe_number) = \
            TupleSort('DataStore', [StringSort(), ArraySort(IntSort(), StringSort()), IntSort()])

# Define the Z3 tuple sort representing data object, containing the following fields:
# participant ID, connected task ID, data object ID, data object name and data object type
data_object_sort, mk_data_object, (participant_id, task_id, object_id, object_name, object_type) = \
            TupleSort("DataObject", [StringSort(), StringSort(), StringSort(), StringSort(), StringSort()])

# Define Z3 tuple representing Potential Evidence Source, containing the following fields:
# evidence source ID, boolean value indicating whether the evidence source has an association
pe_source_sort, mk_pe_source, (pes_id, has_assoc) = TupleSort("PESource", [StringSort(), BoolSort()])

# Define Z3 tuple representing Flow Object, containing the following fields:
# flow object ID, boolean value indicating whether the flow object has a Potential Evidence Source label
flow_object_sort, mk_flow_object, (flow_obj_id, has_pes) = \
            TupleSort("FlowObject", [StringSort(), BoolSort()])
