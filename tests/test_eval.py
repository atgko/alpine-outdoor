"""Tests for the Stage 3 harness: adversarial case file, metrics, and run_eval guards.
No API calls: records come from run_case with the fake client."""
import json
import unittest
from pathlib import Path

from eval import metrics, run_eval
from eval.split import load_cases, load_split
from src.case_facts import from_csv_row
from src.guardrails import VIOLATION_CHECKS
from src.pipeline import INPUT_FIELDS, run_case
from src.rules import evaluate
from src.schema import ROUTES
from tests.test_pipeline import FakeClient, triage_json

ROOT = Path(__file__).resolve().parent.parent
CASES = {r["case_id"]: r for r in load_cases()}
ADVERSARIAL = json.loads((ROOT / "eval" / "adversarial_cases.json").read_text(encoding="utf-8"))["cases"]


def record(case_id: str, version: str = "v2", repeat: int = 1, **overrides) -> dict:
    reply = triage_json(case_id=case_id, **overrides)
    return {"run": "test", "repeat": repeat, **run_case(CASES[case_id], version, FakeClient([reply]), "tune")}


class TestAdversarialCases(unittest.TestCase):
    def test_ten_cases_with_unique_ids_and_all_fields(self):
        self.assertEqual(len(ADVERSARIAL), 10)
        self.assertEqual(len({c["id"] for c in ADVERSARIAL}), 10)
        for c in ADVERSARIAL:
            self.assertEqual(set(c["case"]), set(INPUT_FIELDS), c["id"])
            self.assertEqual(c["case"]["case_id"], c["id"])

    def test_expected_values_are_valid(self):
        for c in ADVERSARIAL:
            exp = c["expected"]
            self.assertIn(exp["route"], ROUTES, c["id"])
            self.assertTrue(set(exp["required_approvals"]) <= set(ROUTES), c["id"])
            self.assertTrue(set(exp["must_not"]) <= set(VIOLATION_CHECKS), c["id"])
            self.assertTrue(exp["must"], c["id"])

    def test_only_the_injection_case_is_marked(self):
        self.assertEqual([c["id"] for c in ADVERSARIAL if c["injection_present"]], ["ADV-09"])

    def test_messages_match_the_order_number_flag(self):
        for c in ADVERSARIAL:
            self.assertEqual("AO-" in c["message"], c["case"]["order_number_provided"] == "Yes", c["id"])

    def test_rule_layer_agrees_with_expected_route_and_approvals(self):
        for c in ADVERSARIAL:
            result = evaluate(from_csv_row(c["case"]))
            self.assertEqual(result.primary_route, c["expected"]["route"], c["id"])
            self.assertEqual(list(result.required_approvals), c["expected"]["required_approvals"], c["id"])

    def test_adversarial_ids_are_not_csv_cases(self):
        self.assertFalse({c["id"] for c in ADVERSARIAL} & set(CASES))


class TestLabels(unittest.TestCase):
    def test_expected_approvals(self):
        self.assertEqual(metrics.expected_approvals(CASES["CS-5246"]), {"Warranty Team", "Support Lead"})
        self.assertEqual(metrics.expected_approvals(CASES["CS-5244"]), set())
        self.assertEqual(metrics.expected_approvals(CASES["CS-5229"]), {"Product Safety"})

    def test_policy_override_only_for_cs5244(self):
        self.assertEqual(metrics.policy_routes(), {"CS-5244": "Support Lead"})

    def test_extraction_subset_is_fixed_and_15(self):
        tune = load_split("tune")
        first, second = metrics.extraction_subset(tune), metrics.extraction_subset(reversed(tune))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 15)
        self.assertTrue(first <= set(tune))


class TestScoring(unittest.TestCase):
    def test_owner_and_policy_views_differ_on_cs5244(self):
        row = metrics.score_records([record("CS-5244", recommended_route="Support Lead",
                                            issue_type="return", required_approvals=["Support Lead"])])[0]
        self.assertFalse(row["owner_match"])
        self.assertTrue(row["policy_match"])

    def test_approval_recall(self):
        ok = record("CS-5246", recommended_route="Warranty Team", required_approvals=["Warranty Team", "Support Lead"])
        miss = record("CS-5246", recommended_route="Warranty Team", required_approvals=["Warranty Team"])
        rows = metrics.score_records([ok, miss])
        self.assertEqual([r["approval_recall_ok"] for r in rows], [True, False])

    def test_missing_order_number_flag(self):
        cid = next(c for c in load_split("tune") if CASES[c]["order_number_provided"] == "No")
        flagged = record(cid, order_number_present=False)
        missed = record(cid, order_number_present=True, missing_information=[])
        rows = metrics.score_records([flagged, missed])
        self.assertEqual([r["missing_order_flagged"] for r in rows], [True, False])
        self.assertIsNone(metrics.score_records([record("CS-5246")])[0]["missing_order_flagged"])

    def test_safety_case_must_route_to_product_safety(self):
        rows = metrics.score_records([record("CS-5229", recommended_route="Support Lead"),
                                      record("CS-5229", recommended_route="Product Safety")])
        self.assertEqual([r["safety_routed_ok"] for r in rows], [False, True])

    def test_guardrails_are_recomputed(self):
        rec = record("CS-5229", draft_reply="It is safe to use.")
        rec["guardrails"] = {"violation_count": 0}  # as if logged by older checks
        self.assertEqual(metrics.score_records([rec])[0]["violations"], "safety_clearance")

    def test_consistency_counts_route_changes(self):
        rows = metrics.score_records([record("CS-5246", repeat=1, recommended_route="Support Lead"),
                                      record("CS-5246", repeat=2, recommended_route="Warranty Team")])
        table = "\n".join(metrics.consistency(rows))
        self.assertIn("| v2 | 1 | 1 | 0 |", table)

    def test_unknown_cases_are_refused(self):
        rec = record("CS-5246")
        rec["case_id"] = "ADV-01"
        with self.assertRaises(SystemExit):
            metrics.score_records([rec])

    def test_tables_state_split_mode_version_model_and_cases(self):
        rows = metrics.score_records([record("CS-5246"), record("CS-5229", version="v3")])
        text = "\n".join(metrics.metrics_tables(rows))
        for part in ("Data split: tune", "Mode: fields_only", "Prompt versions: v2, v3",
                     "Model: fake-model (fake)", "Cases: 2"):
            self.assertIn(part, text)


class TestRunEvalGuards(unittest.TestCase):
    def test_holdout_split_is_refused_without_both_flags(self):
        for flags in ([], ["--holdout"], ["--final"]):
            with self.assertRaises(SystemExit):
                run_eval.main(["--split", "holdout", "--versions", "v1", "--mode", "fields", "--dry-run", *flags])

    def test_case_outside_the_split_is_refused(self):
        holdout_case = load_split("holdout")[0]
        with self.assertRaises(SystemExit):
            run_eval.main(["--split", "tune", "--cases", holdout_case, "--dry-run"])

    def test_dry_run_makes_no_calls(self):
        self.assertIsNone(run_eval.main(["--split", "tune", "--versions", "v1", "--mode", "fields", "--dry-run"]))


if __name__ == "__main__":
    unittest.main()
