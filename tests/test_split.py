"""Tests for the tune and holdout split."""
import unittest
from collections import Counter

from eval.split import load_cases, load_split, make_split

CASES = load_cases()
OWNER = {c["case_id"]: c["assigned_owner"] for c in CASES}


class TestSplit(unittest.TestCase):
    def test_sizes_and_disjoint(self):
        tune, holdout = make_split(CASES)
        self.assertEqual((len(tune), len(holdout)), (28, 20))
        self.assertEqual(set(tune) & set(holdout), set())
        self.assertEqual(set(tune) | set(holdout), set(OWNER))

    def test_deterministic(self):
        self.assertEqual(make_split(CASES), make_split(CASES))

    def test_every_owner_in_both_splits(self):
        tune, holdout = make_split(CASES)
        self.assertEqual(set(Counter(OWNER[c] for c in tune)), set(OWNER.values()))
        self.assertEqual(set(Counter(OWNER[c] for c in holdout)), set(OWNER.values()))

    def test_saved_files_match_code(self):
        tune, holdout = make_split(CASES)
        self.assertEqual(load_split("tune"), tune)
        self.assertEqual(load_split("holdout"), holdout)


if __name__ == "__main__":
    unittest.main()
