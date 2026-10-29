"""Unit tests for the rule layer. Run: python -m unittest discover -s tests -v"""
import unittest
from dataclasses import replace
from pathlib import Path

from src.case_facts import CaseFacts
from src.rules import (
    ALL_RULE_IDS, CANNOT_EVALUATE, CLIENT, CLIENT_RULE_IDS, FIRED, FRAUD,
    FULFILLMENT, LEAD, NOT_FIRED, REP, ROUTE_PRIORITY, RULES, SAFETY, SHIPPING,
    WARRANTY, evaluate,
)

POLICY_FILE = (Path(__file__).resolve().parent.parent / "data"
               / "Alpine_Outdoor_Customer_Support_Policies_and_Knowledge_Resources.md")

# A known-everything baseline where no rule fires. Tests change one or two fields.
QUIET = CaseFacts(
    case_id="TEST",
    issue_type="product_question",
    product_category="Camping equipment",
    order_number_present=True,
    amount_usd=100.0,
    requested_outcome="Information",
    delivery_status="Delivered",
    purchase_channel="online",
    within_30_days=True,
    item_unused=True,
    proof_of_purchase=True,
    protective_item=False,
    defect_or_safety_reported=False,
    fraud_signal_in_text=False,
    prior_related_claims_90d=0,
    fulfillment_error_reported=False,
    days_without_movement=0,
    address_or_account_change=False,
)


def status(facts: CaseFacts, rule_id: str) -> str:
    result = evaluate(facts)
    return next(f.status for f in result.flags if f.rule_id == rule_id)


class TestBaseline(unittest.TestCase):
    def test_quiet_case_fires_nothing_and_uses_default_route(self):
        result = evaluate(QUIET)
        self.assertEqual(result.fired, ())
        self.assertEqual(result.cannot_evaluate, ())
        self.assertEqual(result.primary_route, REP)
        self.assertTrue(result.default_route_used)
        self.assertEqual(result.required_approvals, ())

    def test_client_rule_text_matches_policy_file_exactly(self):
        policy = POLICY_FILE.read_text(encoding="utf-8")
        client_rules = [r for r in RULES if r.origin == CLIENT]
        self.assertEqual(len(client_rules), 9)
        for rule in client_rules:
            condition, outcome = rule.rule_text.split(" | ")
            self.assertIn(f"| {condition} | {outcome} |", policy, rule.id)

    def test_team_proposed_rules_are_labelled(self):
        for rule in RULES:
            if rule.id.startswith("T"):
                self.assertTrue(rule.rule_text.startswith("TEAM PROPOSED"), rule.id)


class TestR1NoOrderNumber(unittest.TestCase):
    def test_fires_when_order_number_missing(self):
        self.assertEqual(status(replace(QUIET, order_number_present=False), "R1"), FIRED)

    def test_not_fired_when_order_number_present(self):
        self.assertEqual(status(QUIET, "R1"), NOT_FIRED)

    def test_cannot_evaluate_when_unknown(self):
        self.assertEqual(status(replace(QUIET, order_number_present=None), "R1"), CANNOT_EVALUATE)


class TestR2StandardReturn(unittest.TestCase):
    ret = replace(QUIET, issue_type="return", requested_outcome="Refund")

    def test_fires_for_unused_online_return_within_30_days(self):
        self.assertEqual(status(self.ret, "R2"), FIRED)
        self.assertEqual(evaluate(self.ret).primary_route, REP)

    def test_not_fired_when_item_used(self):
        self.assertEqual(status(replace(self.ret, item_unused=False), "R2"), NOT_FIRED)

    def test_cannot_evaluate_when_window_unknown(self):
        self.assertEqual(status(replace(self.ret, within_30_days=None), "R2"), CANNOT_EVALUATE)


class TestR3StoreReturn(unittest.TestCase):
    store = replace(QUIET, issue_type="return", purchase_channel="store")

    def test_fires_for_store_return_with_proof(self):
        self.assertEqual(status(self.store, "R3"), FIRED)

    def test_not_fired_for_online_purchase(self):
        self.assertEqual(status(replace(self.store, purchase_channel="online"), "R3"), NOT_FIRED)

    def test_cannot_evaluate_when_channel_unknown(self):
        # purchase_channel is not a CSV column, so this is the common case.
        self.assertEqual(status(replace(self.store, purchase_channel=None), "R3"), CANNOT_EVALUATE)


class TestR4OutsideWindowOrUnclear(unittest.TestCase):
    ret = replace(QUIET, issue_type="return", requested_outcome="Refund")

    def test_fires_outside_window(self):
        facts = replace(self.ret, within_30_days=False)
        self.assertEqual(status(facts, "R4"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, LEAD)

    def test_fires_when_item_used(self):
        self.assertEqual(status(replace(self.ret, item_unused=False), "R4"), FIRED)

    def test_fires_when_condition_unclear(self):
        self.assertEqual(status(replace(self.ret, item_unused=None), "R4"), FIRED)

    def test_not_fired_for_unused_return_within_window(self):
        self.assertEqual(status(self.ret, "R4"), NOT_FIRED)

    def test_not_fired_for_non_return(self):
        self.assertEqual(status(replace(QUIET, within_30_days=False), "R4"), NOT_FIRED)

    def test_cannot_evaluate_when_window_unknown_and_item_unused(self):
        self.assertEqual(status(replace(self.ret, within_30_days=None), "R4"), CANNOT_EVALUATE)


class TestR5DeliveredMissing(unittest.TestCase):
    missing = replace(QUIET, issue_type="missing_shipment", requested_outcome="Refund")

    def test_fires_when_marked_delivered(self):
        self.assertEqual(status(self.missing, "R5"), FIRED)
        self.assertEqual(evaluate(self.missing).primary_route, SHIPPING)

    def test_not_fired_when_in_transit(self):
        self.assertEqual(status(replace(self.missing, delivery_status="In transit"), "R5"), NOT_FIRED)

    def test_cannot_evaluate_without_delivery_status(self):
        self.assertEqual(status(replace(self.missing, delivery_status=None), "R5"), CANNOT_EVALUATE)


class TestR6ClimbingSafety(unittest.TestCase):
    def test_fires_for_climbing_defect(self):
        facts = replace(QUIET, protective_item=True, defect_or_safety_reported=True)
        self.assertEqual(status(facts, "R6"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, SAFETY)

    def test_not_fired_for_climbing_sizing_question(self):
        self.assertEqual(status(replace(QUIET, protective_item=True), "R6"), NOT_FIRED)

    def test_not_fired_for_camping_defect(self):
        self.assertEqual(status(replace(QUIET, defect_or_safety_reported=True), "R6"), NOT_FIRED)


class TestR7HighValue(unittest.TestCase):
    def test_fires_over_500_refund(self):
        facts = replace(QUIET, amount_usd=980.0, requested_outcome="Refund")
        self.assertEqual(status(facts, "R7"), FIRED)
        self.assertEqual(evaluate(facts).required_approvals, (LEAD,))

    def test_not_fired_at_exactly_500(self):
        self.assertEqual(status(replace(QUIET, amount_usd=500.0, requested_outcome="Refund"), "R7"), NOT_FIRED)

    def test_not_fired_for_information_request(self):
        self.assertEqual(status(replace(QUIET, amount_usd=980.0), "R7"), NOT_FIRED)

    def test_cannot_evaluate_without_amount(self):
        self.assertEqual(status(replace(QUIET, amount_usd=None, requested_outcome="Refund"), "R7"),
                         CANNOT_EVALUATE)


class TestR8Fraud(unittest.TestCase):
    def test_fires_for_chargeback_issue_type(self):
        facts = replace(QUIET, issue_type="chargeback")
        self.assertEqual(status(facts, "R8"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, FRAUD)

    def test_fires_for_signal_in_text(self):
        self.assertEqual(status(replace(QUIET, fraud_signal_in_text=True), "R8"), FIRED)

    def test_fires_for_repeated_claims(self):
        self.assertEqual(status(replace(QUIET, prior_related_claims_90d=3), "R8"), FIRED)

    def test_not_fired_when_all_signals_known_negative(self):
        self.assertEqual(status(QUIET, "R8"), NOT_FIRED)

    def test_cannot_evaluate_without_prior_claims_count(self):
        # prior_related_claims_90d is not in the CSV.
        self.assertEqual(status(replace(QUIET, prior_related_claims_90d=None), "R8"), CANNOT_EVALUATE)


class TestR9AddressChange(unittest.TestCase):
    def test_fires_for_address_change(self):
        facts = replace(QUIET, issue_type="account_change", address_or_account_change=True)
        self.assertEqual(status(facts, "R9"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, REP)

    def test_not_fired_otherwise(self):
        self.assertEqual(status(QUIET, "R9"), NOT_FIRED)


class TestW1Warranty(unittest.TestCase):
    def test_fires_for_warranty_claim(self):
        facts = replace(QUIET, issue_type="warranty")
        self.assertEqual(status(facts, "W1"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, WARRANTY)

    def test_not_fired_for_other_issue(self):
        self.assertEqual(status(QUIET, "W1"), NOT_FIRED)


class TestT1FulfillmentError(unittest.TestCase):
    def test_fires_for_fulfillment_error(self):
        facts = replace(QUIET, issue_type="wrong_item", fulfillment_error_reported=True)
        self.assertEqual(status(facts, "T1"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, FULFILLMENT)

    def test_not_fired_otherwise(self):
        self.assertEqual(status(QUIET, "T1"), NOT_FIRED)

    def test_absent_when_disabled(self):
        facts = replace(QUIET, fulfillment_error_reported=True)
        result = evaluate(facts, enabled=CLIENT_RULE_IDS)
        self.assertNotIn("T1", [f.rule_id for f in result.flags])
        self.assertEqual(result.primary_route, REP)


class TestT2StalledShipment(unittest.TestCase):
    stalled = replace(QUIET, issue_type="missing_shipment", days_without_movement=12)

    def test_label_created_routes_to_fulfillment(self):
        facts = replace(self.stalled, delivery_status="Label created")
        self.assertEqual(status(facts, "T2"), FIRED)
        self.assertEqual(evaluate(facts).primary_route, FULFILLMENT)

    def test_in_transit_routes_to_shipping(self):
        facts = replace(self.stalled, delivery_status="In transit")
        self.assertEqual(evaluate(facts).primary_route, SHIPPING)

    def test_not_fired_under_7_days(self):
        facts = replace(self.stalled, delivery_status="In transit", days_without_movement=2)
        self.assertEqual(status(facts, "T2"), NOT_FIRED)

    def test_not_fired_when_delivered(self):
        self.assertEqual(status(self.stalled, "T2"), NOT_FIRED)

    def test_cannot_evaluate_without_day_count(self):
        facts = replace(self.stalled, delivery_status="In transit", days_without_movement=None)
        self.assertEqual(status(facts, "T2"), CANNOT_EVALUATE)


class TestPriorityAndApprovals(unittest.TestCase):
    def test_740_warranty_claim_goes_to_warranty_with_lead_approval(self):
        facts = replace(QUIET, issue_type="warranty", amount_usd=740.0, requested_outcome="Refund")
        result = evaluate(facts)
        self.assertEqual(result.primary_route, WARRANTY)
        self.assertEqual(result.required_approvals, (WARRANTY, LEAD))

    def test_high_value_helmet_goes_to_safety_with_lead_approval(self):
        facts = replace(QUIET, protective_item=True, defect_or_safety_reported=True,
                        amount_usd=540.0, requested_outcome="Refund")
        result = evaluate(facts)
        self.assertEqual(result.primary_route, SAFETY)
        self.assertEqual(result.required_approvals, (SAFETY, LEAD))

    def test_fraud_outranks_everything(self):
        facts = replace(QUIET, issue_type="chargeback", amount_usd=690.0, requested_outcome="Refund",
                        protective_item=True, defect_or_safety_reported=True)
        result = evaluate(facts)
        self.assertEqual(result.primary_route, FRAUD)
        self.assertEqual(result.required_approvals, (FRAUD, SAFETY, LEAD))

    def test_safety_case_without_order_number_still_goes_to_safety(self):
        facts = replace(QUIET, order_number_present=False, protective_item=True,
                        defect_or_safety_reported=True)
        self.assertEqual(evaluate(facts).primary_route, SAFETY)

    def test_priority_order_is_the_team_decision(self):
        self.assertEqual(ROUTE_PRIORITY, (FRAUD, SAFETY, WARRANTY, LEAD, SHIPPING, FULFILLMENT, REP))

    def test_unknown_facts_never_produce_a_fired_flag(self):
        result = evaluate(CaseFacts(case_id="EMPTY"))
        self.assertEqual(result.fired, ())
        self.assertEqual({f.rule_id for f in result.cannot_evaluate}, set(ALL_RULE_IDS))

    def test_result_exposes_no_action_fields(self):
        result = evaluate(QUIET)
        for name in ("action", "refund", "approve", "replacement"):
            self.assertFalse(hasattr(result, name))


if __name__ == "__main__":
    unittest.main()
