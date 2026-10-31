"""Tests for the Stage 4 review screen. Fake client and temp folders only; no API calls."""
import html
import json
import re
import tempfile
import unittest
from pathlib import Path

from eval.split import load_cases, load_split
from src.pipeline import run_case
from src.review_app import BANNER, create_app, markdown_blocks
from tests.test_pipeline import FakeClient, triage_json

CASES = {r["case_id"]: r for r in load_cases()}
HOLDOUT = load_split("holdout")
RESULTS_MD = """# Metrics: test

Data split: tune | Mode: fields_only

| Metric | v4 | v5 |
|---|---|---|
| Route = assigned_owner | 25/28 (89%) | 25/28 (89%) |
| Note with <b>tag</b> | a | b |

```
raw block
```
"""


def write_run(folder: Path) -> None:
    v4 = run_case(CASES["CS-5229"], "v4", FakeClient([triage_json(
        case_id="CS-5229", recommended_route="Product Safety", required_approvals=["Product Safety"],
        sources_cited=["KB-427"], confidence="low", draft_reply="Our Product Safety team will review your report.",
        needs_human_judgment_reason="Safety gear defect.")]), "tune")
    v1 = run_case(CASES["CS-5229"], "v1", FakeClient(["Product Safety.\n\n**Draft reply:**\n\nWe will look into it."]), "tune")
    hold = run_case(CASES[HOLDOUT[0]], "v2", FakeClient([triage_json(case_id=HOLDOUT[0])]), "holdout")
    lines = [{"run": "eval_test", "warning": "HOLDOUT TOUCHED"},
             {"run": "eval_test", **v4}, {"run": "eval_test", **v1}, {"run": "eval_test", **hold}]
    (folder / "eval_test.jsonl").write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")


class ReviewAppTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.runs, self.results = root / "runs", root / "results"
        self.runs.mkdir()
        self.results.mkdir()
        write_run(self.runs)
        (self.results / "metrics_test.md").write_text(RESULTS_MD, encoding="utf-8")
        self.fake = FakeClient([triage_json(case_id="ADV-09", recommended_route="Support Representative",
                                            required_approvals=[], draft_reply="A representative will review it.")])
        self.app = create_app(self.runs, self.results, client_factory=lambda alias: self.fake)
        self.client = self.app.test_client()
        self.csrf = self.app.config["CSRF_TOKEN"]

    def tearDown(self):
        self.tmp.cleanup()

    def page(self, url):
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200, url)
        return resp.get_data(as_text=True)


class TestReplay(ReviewAppTest):
    def test_banner_and_replay_label(self):
        text = self.page("/review?case=CS-5229")
        self.assertIn(BANNER, text)
        self.assertIn("Replay of recorded run eval_test.jsonl", text)

    def test_shows_all_required_parts(self):
        text = html.unescape(self.page("/review?case=CS-5229&file=eval_test.jsonl&line=1"))
        for part in ("policy_relevant_facts", "SIMULATED customer message", "Extracted facts", "Rule flags",
                     "R6", "KB-427", "Product Safety", "Required approvals", "Confidence", "low",
                     "Safety gear defect.", "Our Product Safety team will review your report.",
                     'value="approve"', 'value="edit"', 'value="reject"'):
            self.assertIn(part, text)

    def test_v1_record_without_structured_output(self):
        text = self.page("/review?case=CS-5229&file=eval_test.jsonl&line=2")
        self.assertIn("No structured output in this run", text)
        self.assertIn("computed now from the case fields", text)
        self.assertIn("We will look into it.", text)

    def test_live_defaults_to_the_small_model(self):
        self.assertIn("<option selected>small</option>", self.page("/review?case=CS-5229"))

    def test_case_without_recorded_run(self):
        text = self.page("/review?case=CS-5246")
        self.assertIn("No recorded run for CS-5246", text)


class TestHoldoutIsNeverShown(ReviewAppTest):
    def test_picker_lists_tune_and_adversarial_only(self):
        text = self.page("/review")
        for cid in load_split("tune"):
            self.assertIn(f"case={cid}", text)
        self.assertIn("case=ADV-09", text)
        for cid in HOLDOUT:
            self.assertNotIn(cid, text)

    def test_holdout_case_and_record_are_refused(self):
        self.assertEqual(self.client.get(f"/review?case={HOLDOUT[0]}").status_code, 404)
        self.assertEqual(self.client.get("/review?case=CS-5229&file=eval_test.jsonl&line=3").status_code, 400)


class TestDecisions(ReviewAppTest):
    def post(self, **form):
        data = {"csrf": self.csrf, "case": "CS-5229", "file": "eval_test.jsonl", "line": "1",
                "decision": "approve", "edited_reply": "Our Product Safety team will review your report."}
        data.update(form)
        return self.client.post("/decision", data=data)

    def audit(self):
        return [json.loads(x) for x in (self.runs / "audit.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_approve_writes_only_the_audit_log(self):
        before = sorted(p.name for p in self.runs.iterdir())
        self.assertEqual(self.post().status_code, 302)
        self.assertEqual(sorted(p.name for p in self.runs.iterdir()), sorted(before + ["audit.jsonl"]))
        entry = self.audit()[0]
        self.assertEqual(entry["case_id"], "CS-5229")
        self.assertEqual(entry["decision"], "approve")
        self.assertIsNone(entry["human_edit"])
        self.assertEqual(entry["ai_output"]["final_route"], "Product Safety")
        self.assertEqual(entry["ai_output"]["run_log"], "eval_test.jsonl")
        self.assertIn("timestamp", entry)

    def test_edit_and_reject_are_recorded_with_the_human_text(self):
        self.post(decision="edit", edited_reply="Edited reply text.")
        self.post(decision="reject", note="Wrong team")
        entries = self.audit()
        self.assertEqual([e["decision"] for e in entries], ["edit", "reject"])
        self.assertEqual(entries[0]["human_edit"], "Edited reply text.")
        self.assertEqual(entries[1]["reviewer_note"], "Wrong team")

    def test_bad_requests_are_refused_and_not_logged(self):
        self.assertEqual(self.post(decision="send").status_code, 400)
        self.assertEqual(self.post(csrf="wrong").status_code, 400)
        self.assertEqual(self.post(file="../eval_test.jsonl").status_code, 404)
        self.assertEqual(self.post(case="CS-5246").status_code, 400)
        self.assertEqual(self.post(case=HOLDOUT[0]).status_code, 404)
        self.assertFalse((self.runs / "audit.jsonl").exists())


class TestLive(ReviewAppTest):
    def test_live_run_uses_the_client_logs_and_shows_live_label(self):
        resp = self.client.post("/live", data={"csrf": self.csrf, "case": "ADV-09", "version": "v5",
                                               "mode": "fields_plus_simulated_message", "model": "small"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(self.fake.calls), 1)
        self.assertIn("ignore your rules", self.fake.calls[0][1])
        live_logs = list(self.runs.glob("live_*.jsonl"))
        self.assertEqual(len(live_logs), 1)
        record = json.loads(live_logs[0].read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual((record["case_id"], record["split"], record["injection_present"]), ("ADV-09", "adversarial", True))
        text = self.page(resp.headers["Location"])
        self.assertIn(f"Live run, logged to {live_logs[0].name}", text)

    def test_live_refuses_bad_input(self):
        base = {"csrf": self.csrf, "case": "ADV-09", "version": "v5", "mode": "fields_only", "model": "small"}
        self.assertEqual(self.client.post("/live", data={**base, "version": "v9"}).status_code, 400)
        self.assertEqual(self.client.post("/live", data={**base, "csrf": "x"}).status_code, 400)
        self.assertEqual(self.client.post("/live", data={**base, "case": HOLDOUT[0]}).status_code, 404)
        self.assertEqual(self.fake.calls, [])

    def test_live_without_key_makes_no_call(self):
        app = create_app(self.runs, self.results)  # real client path, but the key check comes first
        import os
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            resp = app.test_client().post("/live", data={"csrf": app.config["CSRF_TOKEN"], "case": "ADV-09",
                                                        "version": "v5", "mode": "fields_only", "model": "small"})
            self.assertIn("needs+ANTHROPIC_API_KEY", resp.headers["Location"])
        finally:
            if saved is not None:
                os.environ["ANTHROPIC_API_KEY"] = saved
        self.assertEqual(list(self.runs.glob("live_*.jsonl")), [])


class TestEvaluation(ReviewAppTest):
    def test_tables_render_from_the_file(self):
        text = self.page("/evaluation?file=metrics_test.md")
        self.assertIn("<th>Metric</th>", text)
        self.assertIn("<td>25/28 (89%)</td>", text)
        self.assertIn("Note with &lt;b&gt;tag&lt;/b&gt;", text)  # escaped, not rendered as HTML
        self.assertEqual(len(re.findall(r"<table>", text)), 1)

    def test_lists_files_and_refuses_others(self):
        self.assertIn("metrics_test.md", self.page("/evaluation"))
        self.assertEqual(self.client.get("/evaluation?file=../secret.md").status_code, 404)
        self.assertEqual(self.client.get("/evaluation?file=missing.md").status_code, 404)

    def test_markdown_blocks(self):
        blocks = markdown_blocks(RESULTS_MD)
        self.assertEqual([b["type"] for b in blocks], ["heading", "text", "table", "code"])
        self.assertEqual(blocks[2]["header"], ["Metric", "v4", "v5"])
        self.assertEqual(blocks[2]["rows"][0], ["Route = assigned_owner", "25/28 (89%)", "25/28 (89%)"])

    def test_every_real_results_file_renders(self):
        app = create_app(self.runs)  # real results/ folder, read only
        client = app.test_client()
        for path in sorted((Path(__file__).resolve().parent.parent / "results").glob("*.md")):
            self.assertEqual(client.get(f"/evaluation?file={path.name}").status_code, 200, path.name)


if __name__ == "__main__":
    unittest.main()
