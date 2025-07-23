"""
Storage Module for Large-Scale Protein Data

This module provides efficient storage solutions for massive protein datasets
(250M+ proteins) with hierarchical organization, chunking, and compression.
"""

import os
import h5py
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional, Tuple

class ProteinStorage:
    """
    Minimal storage system for protein families: embeddings and metadata only.
    """
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.family_dir = self.base_dir / "families"
        self.metadata_dir = self.base_dir / "metadata"
        self.family_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def store_family_embeddings(self, family_id: str, embeddings: np.ndarray, protein_ids: List[str], metadata: Optional[pd.DataFrame] = None) -> str:
        """
        Store embeddings and protein IDs for a family. Optionally store metadata.
        """
        if embeddings.dtype != np.uint8:
            raise ValueError("Embeddings must be np.uint8 for binary storage.")
        family_file = self.family_dir / f"family_{family_id}.h5"
        with h5py.File(family_file, 'w') as f:
            f.create_dataset('embeddings', data=embeddings, compression='gzip', chunks=True)
            dt = h5py.string_dtype(encoding='utf-8')
            f.create_dataset('protein_ids', data=np.array(protein_ids, dtype=object), dtype=dt)
            f.attrs['num_proteins'] = len(protein_ids)
            f.attrs['embedding_dim'] = embeddings.shape[1]
        if metadata is not None:
            metadata_file = self.metadata_dir / f"family_{family_id}_metadata.parquet"
            metadata.to_parquet(metadata_file, compression='gzip')
        return str(family_file)

    def load_family_embeddings(self, family_id: str) -> Tuple[np.ndarray, List[str]]:
        """
        Load embeddings and protein IDs for a family.
        """
        family_file = self.family_dir / f"family_{family_id}.h5"
        with h5py.File(family_file, 'r') as f:
            embeddings = f['embeddings'][:]
            protein_ids = [pid.decode('utf-8') if isinstance(pid, bytes) else pid for pid in f['protein_ids'][:]]
        return embeddings, protein_ids

    def load_metadata(self, family_id: str) -> pd.DataFrame:
        """
        Load metadata for a family. Returns DataFrame indexed by uniprot_id.
        """
        metadata_file = self.metadata_dir / f"family_{family_id}_metadata.parquet"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
        return pd.read_parquet(metadata_file)

    def get_family_list(self) -> List[str]:
        """
        Get list of all available family IDs.
        """
        family_files = list(self.family_dir.glob("family_*.h5"))
        return [f.stem.replace("family_", "") for f in family_files]  # Return '18', etc. 