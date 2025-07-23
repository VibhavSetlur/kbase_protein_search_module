# Minimal KBase Protein Lookup App

This repository provides a minimal KBase app for protein lookup by UniProt ID. Given a UniProt ID, the app checks if the protein exists in the local storage and, if found, returns its family, metadata, and embedding.

## Features
- **Check existence** of a protein by UniProt ID
- **Retrieve protein embedding** if found
- **Return family and metadata** for the protein

## Usage
- Deploy as a KBase app or run the server locally.
- Use the UI or JSON-RPC to call the method:
  - `get_protein_embedding_by_uniprot_id` with parameter `protein_id` (string)
- Returns: `exists`, `family_id`, `metadata`, `embedding` (list), and a summary.

## Directory Structure
- `lib/kbase_protein_network_analysis_toolkit/` — Core logic (storage, existence check, API)
- `ui/narrative/methods/CheckProteinExistence/` — UI for the single app method
- `test/unit_tests/` — Unit tests for storage and existence check

## Quickstart
1. Build the Docker image:
   ```bash
   docker build -t protein-lookup .
   ```
2. Run the server:
   ```bash
   docker run -p 9999:9999 protein-lookup
   ```
3. Call the API (example):
   ```json
   {
     "method": "kbase_protein_network_analysis_toolkit.get_protein_embedding_by_uniprot_id",
     "params": [{"protein_id": "P12345"}],
     "version": "1.1",
     "id": "1"
   }
   ```

## Testing
- Run unit tests with:
  ```bash
  pytest test/unit_tests/
  ```

## License
MIT
