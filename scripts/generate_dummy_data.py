import os
import shutil
import numpy as np
import pandas as pd
import h5py
import pyarrow as pa
import pyarrow.parquet as pq
import random

# Configurable parameters
N_FAMILIES = 50
N_PROTEINS_PER_FAMILY = 500
EMBEDDING_DIM = 320  # Must be multiple of 8
DATA_DIR = 'data'

np.random.seed(42)
random.seed(42)

# Remove existing data directory if it exists
if os.path.exists(DATA_DIR):
    shutil.rmtree(DATA_DIR)

families_dir = os.path.join(DATA_DIR, 'families')
metadata_dir = os.path.join(DATA_DIR, 'metadata')
os.makedirs(families_dir, exist_ok=True)
os.makedirs(metadata_dir, exist_ok=True)

def generate_uniprot_id():
    # Generate a realistic UniProt-like accession (6 chars, e.g., P12345, Q9XYZ1)
    first = random.choice('OPQ')
    rest = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
    return first + rest

organisms = ['Homo sapiens', 'Escherichia coli', 'Saccharomyces cerevisiae', 'Arabidopsis thaliana', 'Mus musculus']
functions = ['Kinase', 'Transcription factor', 'Transporter', 'Hydrolase', 'Ligase', 'Oxidoreductase']

for fam in range(N_FAMILIES):
    family_id = f'family_{fam}'
    # Generate unique UniProt-like IDs
    protein_ids = set()
    while len(protein_ids) < N_PROTEINS_PER_FAMILY:
        protein_ids.add(generate_uniprot_id())
    protein_ids = list(protein_ids)
    # Generate random binary embeddings (np.uint8, shape [N, D//8])
    embeddings = np.random.randint(0, 256, size=(N_PROTEINS_PER_FAMILY, EMBEDDING_DIM // 8), dtype=np.uint8)
    # Save HDF5 file
    h5_path = os.path.join(families_dir, f'{family_id}.h5')
    with h5py.File(h5_path, 'w') as f:
        f.create_dataset('embeddings', data=embeddings, compression='gzip', chunks=True)
        dt = h5py.string_dtype(encoding='utf-8')
        f.create_dataset('protein_ids', data=np.array(protein_ids, dtype=object), dtype=dt)
        f.attrs['num_proteins'] = N_PROTEINS_PER_FAMILY
        f.attrs['embedding_dim'] = EMBEDDING_DIM // 8
        f.attrs['chunk_size'] = N_PROTEINS_PER_FAMILY
        f.attrs['compression'] = 'gzip'
        f.attrs['metadata_file'] = os.path.join('metadata', f'{family_id}_metadata.parquet')
    # Create metadata DataFrame
    metadata = pd.DataFrame({
        'uniprot_id': protein_ids,
        'protein_name': [f'Protein {i}' for i in range(N_PROTEINS_PER_FAMILY)],
        'organism': [random.choice(organisms) for _ in range(N_PROTEINS_PER_FAMILY)],
        'function': [random.choice(functions) for _ in range(N_PROTEINS_PER_FAMILY)],
        'family_id': str(fam)
    }).set_index('uniprot_id')
    # Save as Parquet
    meta_path = os.path.join(metadata_dir, f'{family_id}_metadata.parquet')
    table = pa.Table.from_pandas(metadata)
    pq.write_table(table, meta_path)
    print(f"Wrote {h5_path} and {meta_path}")

print(f"Dummy data generated in '{DATA_DIR}' for {N_FAMILIES} families.") 