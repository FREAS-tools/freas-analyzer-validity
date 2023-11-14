from typing import List, Optional

from src.elements.artefact.data_store.data_store import DataStore


class EvidenceDataStore(DataStore):
    """
    Represents a BPMN4FRSS Evidence Data Store.
    """
    def __init__(self, elem_id: str, name: Optional[str] = None):
        """
        Constructor for DataStore class.

        Parameters:
            elem_id (str): Element id
            name (Optional[str]): Element name

        stored_pe (List[str]): List of Data Objects stored in the Evidence Data Store
            representing potential evidence
        """
        super().__init__(elem_id, name)

        self.stored_pe: List[str] = []
