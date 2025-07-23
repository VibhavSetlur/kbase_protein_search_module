import unittest
from kbase_protein_network_analysis_toolkit.storage import ProteinStorage
from kbase_protein_network_analysis_toolkit.check_existence import ProteinExistenceChecker

class TestProteinExistenceChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use the real data directory
        cls.storage = ProteinStorage(base_dir="data")
        cls.checker = ProteinExistenceChecker(storage=cls.storage)
        # Pick a real family and protein from the dummy data
        families = cls.storage.get_family_list()
        assert families, "No families found in data directory"
        cls.family_id = families[0]
        _, protein_ids = cls.storage.load_family_embeddings(cls.family_id)
        assert protein_ids, "No protein IDs found in family"
        cls.real_protein_id = protein_ids[0]
        cls.fake_protein_id = "NOT_A_REAL_UNIPROT_ID"

    def test_protein_exists(self):
        result = self.checker.check_protein_existence(self.real_protein_id)
        self.assertTrue(result["exists"])
        self.assertEqual(result["family_id"], self.family_id)
        self.assertIsInstance(result["metadata"], dict)
        self.assertEqual(result["metadata"]["family_id"], self.family_id)

    def test_protein_not_exists(self):
        result = self.checker.check_protein_existence(self.fake_protein_id)
        self.assertFalse(result["exists"])
        self.assertIsNone(result["family_id"])
        self.assertIsNone(result["metadata"])

    def test_empty_protein_id(self):
        with self.assertRaises(ValueError):
            self.checker.check_protein_existence("")

if __name__ == '__main__':
    unittest.main() 