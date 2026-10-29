"""Tests for the Stage 1 keyword reader and CSV mapping."""
import unittest

from eval.split import load_cases
from src.case_facts import (
    EXTRACTED, INFERRED, ISSUE_TYPE_MAP, STRUCTURED, from_csv_row,
    read_days_without_movement, read_item_unused, read_within_30_days,
)

CASES = {row["case_id"]: row for row in load_cases()}


def facts(case_id):
    return from_csv_row(CASES[case_id])


class TestCsvShape(unittest.TestCase):
    def test_48_cases_and_17_columns(self):
        self.assertEqual(len(CASES), 48)
        self.assertEqual(len(next(iter(CASES.values()))), 17)

    def test_dictionary_columns_missing_from_csv_are_not_invented(self):
        columns = set(next(iter(CASES.values())))
        for missing in ("purchase_channel", "delivery_date", "case_received_date", "prior_related_claims_90d"):
            self.assertNotIn(missing, columns)
        self.assertIsNone(facts("CS-5201").prior_related_claims_90d)
        self.assertIsNone(facts("CS-5201").proof_of_purchase)

    def test_every_csv_issue_type_is_mapped(self):
        for row in CASES.values():
            self.assertIn(row["issue_type"], ISSUE_TYPE_MAP)


class TestKeywordReader(unittest.TestCase):
    def test_within_30_days(self):
        self.assertTrue(read_within_30_days("Within 30 days and tags attached"))
        self.assertTrue(read_within_30_days("order is 4 days old"))
        self.assertFalse(read_within_30_days("Return request is 62 days after delivery"))
        self.assertFalse(read_within_30_days("Return request is outside window"))
        self.assertIsNone(read_within_30_days("Duplicate item was ordered by mistake"))

    def test_item_unused(self):
        self.assertTrue(read_item_unused("Unused trekking poles"))
        self.assertTrue(read_item_unused("item is unopened"))
        self.assertFalse(read_item_unused("Item was washed once and tags removed"))
        self.assertFalse(read_item_unused("tent was used on one trip"))
        self.assertIsNone(read_item_unused("Tent pole arrived bent"))

    def test_days_without_movement(self):
        self.assertEqual(read_days_without_movement("Order has not moved for 12 days"), 12)
        self.assertEqual(read_days_without_movement("Tracking has no movement after 9 days"), 9)
        self.assertIsNone(read_days_without_movement("in transit for two days longer than estimate"))


class TestFromCsvRow(unittest.TestCase):
    def test_structured_fields(self):
        f = facts("CS-5209")
        self.assertEqual(f.issue_type, "refund")
        self.assertEqual(f.amount_usd, 980.0)
        self.assertTrue(f.order_number_present)
        self.assertEqual(f.sources["amount_usd"], STRUCTURED)

    def test_no_order_case(self):
        f = facts("CS-5227")
        self.assertFalse(f.order_number_present)
        self.assertIsNone(f.delivery_status)
        self.assertIsNone(f.purchase_channel)

    def test_purchase_channel_is_labelled_inferred(self):
        self.assertEqual(facts("CS-5201").purchase_channel, "online")
        self.assertEqual(facts("CS-5201").sources["purchase_channel"], INFERRED)

    def test_text_facts_are_labelled_extracted(self):
        f = facts("CS-5244")
        self.assertFalse(f.item_unused)
        self.assertEqual(f.sources["item_unused"], EXTRACTED)

    def test_climbing_defect_detected(self):
        self.assertTrue(facts("CS-5208").defect_or_safety_reported)
        self.assertTrue(facts("CS-5208").protective_item)

    def test_climbing_question_is_not_a_defect(self):
        self.assertFalse(facts("CS-5205").defect_or_safety_reported)

    def test_fraud_signals(self):
        self.assertTrue(facts("CS-5234").fraud_signal_in_text)
        self.assertTrue(facts("CS-5248").fraud_signal_in_text)
        # Team decision 6: changed return reason is not treated as a fraud signal.
        self.assertFalse(facts("CS-5213").fraud_signal_in_text)

    def test_duplicate_keyword_is_a_known_false_positive(self):
        # CS-5225 is a customer ordering twice, but the keyword reader cannot tell.
        self.assertTrue(facts("CS-5225").fulfillment_error_reported)


if __name__ == "__main__":
    unittest.main()
