"""
Protein Existence Checker Module

This module provides a fast method to check if a protein (by UniProt ID)
exists in the storage system, and returns its family and metadata if found.
Integrates with the storage and workflow modules for seamless pipeline use.
"""

import logging
from typing import Optional, Dict, Any
from kbase_protein_network_analysis_toolkit.storage import ProteinStorage

logger = logging.getLogger(__name__)

class ProteinExistenceChecker:
    """
    Checks if a protein exists in the storage and returns its family and metadata.
    """
    def __init__(self, storage: Optional[ProteinStorage] = None, base_dir: str = "data"):
        if storage is not None:
            self.storage = storage
        else:
            self.storage = ProteinStorage(base_dir=base_dir)
        self.family_list = self.storage.get_family_list()

    def check_protein_existence(self, protein_id: str) -> Dict[str, Any]:
        """
        Check if a protein exists by UniProt ID.
        Returns: Dict with keys: exists (bool), family_id (str or None), metadata (dict or None)
        """
        if not protein_id:
            raise ValueError("Must provide a protein_id (UniProt ID).")
        for family_id in self.family_list:
            try:
                metadata = self.storage.load_metadata(family_id)
                if protein_id in metadata.index:
                    return {
                        "exists": True,
                        "family_id": family_id,
                        "metadata": metadata.loc[protein_id].to_dict()
                    }
            except Exception as e:
                logger.debug(f"Error checking family {family_id}: {e}")
                continue
        return {"exists": False, "family_id": None, "metadata": None} 