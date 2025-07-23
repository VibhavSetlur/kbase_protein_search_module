import unittest
import numpy as np
import pandas as pd
from kbase_protein_network_analysis_toolkit.storage import ProteinStorage

class TestProteinStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = ProteinStorage(base_dir="data")
        families = cls.storage.get_family_list()
        assert families, "No families found in data directory"
        cls.family_id = families[0]
        cls.embeddings, cls.protein_ids = cls.storage.load_family_embeddings(cls.family_id)
        cls.metadata = cls.storage.load_metadata(cls.family_id)

    def test_load_family_embeddings(self):
        self.assertTrue(self.embeddings.shape[0] == len(self.protein_ids))
        self.assertTrue(isinstance(self.protein_ids, list))

    def test_load_metadata(self):
        self.assertTrue(list(self.metadata.index) == self.protein_ids)
        self.assertIn("protein_name", self.metadata.columns)

if __name__ == '__main__':
    unittest.main() 