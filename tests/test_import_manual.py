"""Tests for the manual spot check import. No API calls; logs go to a temp folder."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from eval import metrics
from eval.import_manual import ROOT, import_manual, read_rows
from eval.rescore_guardrails import load_records
from eval.split import load_split
from tests.test_pipeline import triage_json

FIELDS = ["case_id", "output", "draft_reply", "recommended_route", "required_approvals", "model", "prompt_version"]


def write_csv(folder: str, rows: list[dict]) -> Path:
    path = Path(folder) / "spot.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{k: r.get(k, "") for k in FIELDS} for r in rows])
    return path


ROWS = [
    {"case_id": "CS-5246", "output": triage_json(recommended_route="Warranty Team",
                                                 required_approvals=["Warranty Team", "Support Lead"])},
    {"case_id": "CS-5229",
     "output": "Route to Product Safety. No fraud or shipping issue here.\nDraft: Thanks for the photos.",
     "draft_reply": "Thanks for the photos. Our Product Safety team will review them."},
    {"case_id": "CS-5244", "output": "Send to Support Lead.\n\n**Draft reply:**\n\nThe jacket is still eligible.",
     "prompt_version": "v1", "model": "gpt-test"},
]


class TestImport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log, self.records = import_manual(write_csv(self.tmp.name, ROWS), "ChatGPT", runs_dir=Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_records_are_labeled_manual(self):
        self.assertTrue(all(r["mode"] == "manual spot check" for r in self.records))
        self.assertEqual([r["split"] for r in self.records], ["tune", "tune", "tune"])
        self.assertEqual([r["provider"] for r in self.records], ["ChatGPT"] * 3)
        self.assertEqual(self.records[2]["model"], "gpt-test")
        self.assertEqual([r["prompt_version"] for r in self.records], ["manual", "manual", "v1"])

    def test_json_output_is_parsed(self):
        r = self.records[0]
        self.assertTrue(r["schema_valid"])
        self.assertEqual(r["final_route"], "Warranty Team")
        self.assertEqual(r["final_required_approvals"], ["Warranty Team", "Support Lead"])

    def test_free_text_route_and_draft_column(self):
        r = self.records[1]
        self.assertIsNone(r["schema_valid"])
        self.assertEqual(r["final_route"], "Product Safety")
        self.assertEqual(r["guardrails"]["violation_count"], 0)  # "fraud" is only in the routing note

    def test_v1_reply_section_is_checked(self):
        r = self.records[2]
        self.assertEqual(r["guardrail_text_source"], "v1_reply_section")
        self.assertTrue(r["guardrails"]["washed_return_eligibility"])

    def test_metrics_recompute_matches_import(self):
        rows = metrics.score_records(load_records(self.log))
        self.assertEqual([r["violation_count"] for r in rows],
                         [r["guardrails"]["violation_count"] for r in self.records])
        self.assertEqual([r["mode"] for r in rows], ["manual spot check"] * 3)
        self.assertIn("Mode: manual spot check", "\n".join(metrics.metrics_tables(rows)))

    def test_log_has_a_note_line(self):
        first = json.loads(self.log.read_text(encoding="utf-8").splitlines()[0])
        self.assertIn("manual spot check", first["note"])


class TestRefusals(unittest.TestCase):
    def refuse(self, rows, **flags):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                import_manual(write_csv(tmp, rows), "ChatGPT", runs_dir=Path(tmp), **flags)

    def test_bad_rows_are_refused(self):
        self.refuse([{"case_id": "CS-9999", "output": "x"}])
        self.refuse([{"case_id": "CS-5246"}])
        self.refuse([{"case_id": "CS-5246", "output": "x", "recommended_route": "Billing"}])
        self.refuse([{"case_id": "CS-5246", "output": "x", "required_approvals": "Support Lead; Billing"}])

    def test_holdout_needs_both_flags(self):
        row = [{"case_id": load_split("holdout")[0], "output": "Support Representative"}]
        self.refuse(row)
        self.refuse(row, holdout=True)
        with tempfile.TemporaryDirectory() as tmp:
            log, _ = import_manual(write_csv(tmp, row), "ChatGPT", True, True, runs_dir=Path(tmp))
            self.assertIn("HOLDOUT TOUCHED", log.read_text(encoding="utf-8"))

    def test_template_is_valid(self):
        self.assertEqual(len(read_rows(ROOT / "eval" / "manual_spot_check_template.csv")), 1)


if __name__ == "__main__":
    unittest.main()
