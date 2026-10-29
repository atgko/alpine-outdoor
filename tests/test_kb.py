"""Tests for the KB loader and source selection."""
import unittest

from src.kb import load_kb, select_sources

KB = load_kb()


class TestLoadKB(unittest.TestCase):
    def test_all_sources_present(self):
        expected = {
            "POL-RETURN", "POL-WARRANTY-SAFETY", "POL-SHIPPING", "POL-GOVERNANCE",
            "NOTE-KNOWLEDGE-QUALITY",
            "KB-101", "KB-205", "KB-318", "KB-427", "KB-510", "KB-612", "KB-710",
        }
        self.assertEqual(set(KB), expected)

    def test_metadata_kept(self):
        self.assertEqual(KB["KB-427"].last_reviewed, "2026-10-03")
        self.assertEqual(KB["KB-427"].owner, "Product Safety")
        self.assertEqual(KB["KB-710"].last_reviewed, "2025-02-01")

    def test_only_kb_710_is_non_authoritative(self):
        self.assertFalse(KB["KB-710"].authoritative)
        others = [s for s in KB.values() if s.id != "KB-710"]
        self.assertTrue(all(s.authoritative for s in others))

    def test_body_copied_from_policy_file(self):
        self.assertIn("Do not instruct the customer to continue using the product.", KB["KB-427"].body)


class TestSelectSources(unittest.TestCase):
    def test_return_gets_return_policy_and_label_article(self):
        ids = select_sources("return", "Within 30 days and tags attached")
        self.assertEqual(ids, ("NOTE-KNOWLEDGE-QUALITY", "POL-RETURN", "KB-101"))

    def test_washed_jacket_adds_kb_510(self):
        self.assertIn("KB-510", select_sources("return", "Item was washed once and tags removed"))

    def test_carabiner_adds_climbing_safety(self):
        ids = select_sources("damaged", "Carabiner gate does not close correctly")
        self.assertIn("KB-427", ids)
        self.assertIn("POL-WARRANTY-SAFETY", ids)

    def test_address_change_includes_kb_710(self):
        self.assertIn("KB-710", select_sources("account_change", "change delivery address"))

    def test_no_duplicates(self):
        ids = select_sources("product_safety", "rope abrasion on climbing rope")
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
