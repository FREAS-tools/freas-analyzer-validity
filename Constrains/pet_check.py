from Elements.Element.element import Element
from Elements.PESource.pe_source import PotentialEvidenceSource
from Elements.Artefact.data_object import PotentialEvidenceType
from Elements.DataReference.data_reference import DataObjectReference

from Constrains.base_sorts import *

from typing import Dict


# if we have an association which is produced from pes
# then data reference should point to the data object
# that has potential evidence type

# only associations produced from pes
# those associations have to have data object reference (data store can't be pet)

def check_pet(elements: Dict[str, Element]) -> Solver:
    s = Solver()

    is_pet = Function("is_pet", DataObjectSort, BoolSort())
    data_object = Const("data_object", DataObjectSort)
    s.add(ForAll(data_object, is_pet(data_object)))

    for key, value in elements.items():
        if isinstance(value, PotentialEvidenceSource) and \
                value.association is not None:
            data_obj_ref = elements[value.association.target_ref]

            assert isinstance(data_obj_ref, DataObjectReference)

            data_ref = elements[data_obj_ref.data_ref]
            data_obj = Const(data_ref.id, DataObjectSort)

            if isinstance(data_ref, PotentialEvidenceType):
                s.add(is_pet(data_obj))
            else:
                s.add((Not(is_pet(data_obj))))

    return s
