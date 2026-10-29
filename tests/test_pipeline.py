"""Pipeline, schema and run guard tests. A fake client stands in for the API."""
import csv
import json
import unittest
from dataclasses import dataclass, field
from pathlib import Path

from eval.guards import GuardError, check_holdout, check_spend, estimate_calls
from eval.split import load_cases
from src.llm import LLMResponse
from src.pipeline import INPUT_FIELDS, VERSIONS, build_inputs, load_prompt, route_from_text, run_case
from src.schema import parse_output

CASES = {r["case_id"]: r for r in load_cases()}
ROOT = Path(__file__).resolve().parent.parent


def triage_json(**overrides) -> str:
    body = {
        "case_id": "CS-5246", "issue_type": "warranty", "product_category": "Camping equipment",
        "order_number_present": True, "missing_information": [], "customer_requested_outcome": "Refund",
        "key_facts": ["Mechanism failed after 21 months"], "rule_flags": ["W1", "R7"],
        "recommended_route": "Support Lead", "required_approvals": ["Support Lead"],
        "sources_cited": ["KB-318"], "confidence": "low",
        "needs_human_judgment_reason": "Warranty coverage and high value.",
        "draft_reply": "Thank you. The Warranty Team will review your claim.",
        "draft_case_note": "Warranty review plus Support Lead approval over $500.",
    }
    return json.dumps({**body, **overrides})


@dataclass
class FakeClient:
    replies: list
    calls: list = field(default_factory=list)

    def call(self, system: str, user: str) -> LLMResponse:
        self.calls.append((system, user))
        text = self.replies[min(len(self.calls), len(self.replies)) - 1]
        return LLMResponse(ok=True, text=text, provider="fake", model="fake-model",
                           input_tokens=100, output_tokens=50, attempts=1)


class TestPrompts(unittest.TestCase):
    def test_all_versions_load_with_system_and_user(self):
        for v in VERSIONS:
            p = load_prompt(v)
            self.assertTrue(p.system and p.user and len(p.sha256) == 12, v)

    def test_labels_never_reach_the_prompt(self):
        row = CASES["CS-5246"]
        for v in VERSIONS:
            _, user, *_ = build_inputs(v, row, None)
            for label in ("required_next_step", "assigned_owner", "resolution_hours", "followups"):
                self.assertNotIn(label, user, v)
            self.assertNotIn(row["required_next_step"], user, v)
        self.assertNotIn("assigned_owner", INPUT_FIELDS)

    def test_no_unfilled_placeholders(self):
        for v in VERSIONS:
            _, user, *_ = build_inputs(v, CASES["CS-5244"], "test message")
            self.assertNotIn("{{", user, v)

    def test_sources_only_in_v3_and_v4(self):
        for v, expected in (("v1", False), ("v2", False), ("v3", True), ("v4", True)):
            _, user, sources, _ = build_inputs(v, CASES["CS-5244"], None)
            self.assertEqual("KB-510" in user, expected, v)
            self.assertEqual(bool(sources), expected, v)

    def test_rules_only_in_v4(self):
        _, user, _, rules = build_inputs("v4", CASES["CS-5246"], None)
        self.assertIn("Primary route from rule layer: Warranty Team", user)
        self.assertIsNotNone(rules)
        self.assertIsNone(build_inputs("v3", CASES["CS-5246"], None)[3])


class TestRunCase(unittest.TestCase):
    def test_v4_overrides_model_route_and_logs_disagreement(self):
        rec = run_case(CASES["CS-5246"], "v4", FakeClient([triage_json()]), "tune")
        self.assertEqual(rec["model_route"], "Support Lead")
        self.assertEqual(rec["final_route"], "Warranty Team")
        self.assertTrue(rec["model_disagreed_with_rules"])
        self.assertEqual(rec["final_required_approvals"][:2], ["Warranty Team", "Support Lead"])

    def test_v4_agreement_is_logged_as_false(self):
        rec = run_case(CASES["CS-5246"], "v4", FakeClient([triage_json(recommended_route="Warranty Team")]), "tune")
        self.assertFalse(rec["model_disagreed_with_rules"])

    def test_v3_has_no_override(self):
        rec = run_case(CASES["CS-5246"], "v3", FakeClient([triage_json()]), "tune")
        self.assertEqual(rec["final_route"], "Support Lead")
        self.assertIsNone(rec["model_disagreed_with_rules"])

    def test_invalid_json_is_retried_once_then_succeeds(self):
        client = FakeClient(["not json", triage_json()])
        rec = run_case(CASES["CS-5246"], "v2", client, "tune")
        self.assertEqual(len(client.calls), 2)
        self.assertTrue(rec["schema_valid"])
        self.assertTrue(rec["schema_retry_used"])
        self.assertEqual(len(rec["raw_outputs"]), 2)

    def test_invalid_twice_is_a_logged_failure(self):
        client = FakeClient(["not json", '{"case_id": "x"}'])
        rec = run_case(CASES["CS-5246"], "v2", client, "tune")
        self.assertEqual(len(client.calls), 2)
        self.assertFalse(rec["schema_valid"])
        self.assertIsNotNone(rec["schema_error"])
        self.assertIsNone(rec["final_route"])

    def test_v4_still_enforces_rules_when_output_invalid(self):
        rec = run_case(CASES["CS-5246"], "v4", FakeClient(["bad", "bad"]), "tune")
        self.assertEqual(rec["final_route"], "Warranty Team")
        self.assertIsNone(rec["model_disagreed_with_rules"])

    def test_v1_route_read_from_text(self):
        rec = run_case(CASES["CS-5229"], "v1", FakeClient(["Route to Product Safety. Draft: ..."]), "tune")
        self.assertEqual(rec["model_route"], "Product Safety")
        self.assertIsNone(rec["schema_valid"])

    def test_guardrails_run_on_draft(self):
        reply = triage_json(draft_reply="Your refund has been approved.")
        rec = run_case(CASES["CS-5246"], "v3", FakeClient([reply]), "tune")
        self.assertTrue(rec["guardrails"]["promises_action"])

    def test_message_mode_recorded(self):
        rec = run_case(CASES["CS-5246"], "v2", FakeClient([triage_json()]), "tune", message="hello")
        self.assertEqual(rec["mode"], "fields_plus_simulated_message")
        self.assertIn('<customer_message simulated="true">', rec["input"]["user"])


class TestSchema(unittest.TestCase):
    def test_accepts_fenced_json(self):
        parsed, err = parse_output("```json\n" + triage_json() + "\n```")
        self.assertIsNone(err)
        self.assertEqual(parsed.recommended_route, "Support Lead")

    def test_rejects_unknown_route(self):
        parsed, err = parse_output(triage_json(recommended_route="Billing"))
        self.assertIsNone(parsed)
        self.assertIn("schema validation failed", err)

    def test_rejects_extra_field(self):
        self.assertIsNone(parse_output(triage_json(extra="x"))[0])

    def test_route_from_text_takes_first_mention(self):
        self.assertEqual(route_from_text("Send to Support Lead, not Product Safety"), "Support Lead")
        self.assertIsNone(route_from_text("no team named"))


class TestGuards(unittest.TestCase):
    def test_holdout_refused_without_flags(self):
        with self.assertRaises(GuardError):
            check_holdout(["CS-5201"], holdout=False, final=False)
        with self.assertRaises(GuardError):
            check_holdout(["CS-5201"], holdout=True, final=False)

    def test_holdout_allowed_with_both_flags_and_warns(self):
        self.assertEqual(len(check_holdout(["CS-5201"], holdout=True, final=True)), 1)

    def test_tune_cases_pass_without_warning(self):
        self.assertEqual(check_holdout(["CS-5246", "CS-5229"], False, False), [])

    def test_estimate_counts_schema_retries(self):
        self.assertEqual(estimate_calls(3, ["v1", "v2", "v3", "v4"], 2), (24, 42))

    def test_spend_guard_needs_yes_above_200(self):
        with self.assertRaises(GuardError):
            check_spend(150, 250, yes=False)
        check_spend(150, 250, yes=True)
        check_spend(100, 200, yes=False)


class TestSimulatedMessages(unittest.TestCase):
    def test_one_simulated_message_per_case(self):
        with (ROOT / "data" / "simulated_messages.csv").open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(sorted(r["case_id"] for r in rows), sorted(CASES))
        self.assertTrue(all(r["simulated"] == "true" for r in rows))
        messy = sum(r["messy"] == "true" for r in rows)
        self.assertTrue(14 <= messy <= 18, messy)

    def test_no_order_number_in_messages_for_cases_without_one(self):
        with (ROOT / "data" / "simulated_messages.csv").open(encoding="utf-8") as fh:
            rows = {r["case_id"]: r["message"] for r in csv.DictReader(fh)}
        for cid, row in CASES.items():
            self.assertEqual("AO-" in rows[cid], row["order_number_provided"] == "Yes", cid)


if __name__ == "__main__":
    unittest.main()
