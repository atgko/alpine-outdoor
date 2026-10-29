"""Tests for the guardrail phrase checks: one violating and one clean example each."""
import unittest

from src.guardrails import check_draft, check_sources

CLEAN = ("Thank you for reaching out. A representative will review your order and the "
         "applicable policy, and we will follow up with the next steps.")


class TestPromisesAction(unittest.TestCase):
    def test_flags_promised_refund(self):
        for text in ("We have issued your refund.", "Your refund has been approved.",
                     "We'll send you a replacement tent today.", "You will receive a full refund.",
                     "We've updated your delivery address.", "Your warranty claim has been approved.",
                     "Don't worry, we have issued your refund."):
            self.assertTrue(check_draft(text)["promises_action"], text)

    def test_clean_and_negated_text_passes(self):
        for text in (CLEAN, "We cannot issue a refund until the review is complete.",
                     "We are not able to approve a replacement in this reply.",
                     "Any refund requires Support Lead approval first."):
            self.assertEqual(check_draft(text)["promises_action"], [], text)


class TestSafetyAdvice(unittest.TestCase):
    def test_flags_continue_using_and_inspection(self):
        for text in ("You can continue using the harness until then.", "It should be safe to use.",
                     "Please inspect the gate for debris."):
            self.assertTrue(check_draft(text)["safety_advice"], text)

    def test_stop_use_is_allowed(self):
        text = "Please do not continue using the carabiner. Product Safety will review your report."
        self.assertEqual(check_draft(text)["safety_advice"], [])


class TestFraudCriteria(unittest.TestCase):
    def test_flags_criteria(self):
        for text in ("Your account was flagged because of multiple refund requests.",
                     "Our fraud team is reviewing this."):
            self.assertTrue(check_draft(text)["reveals_fraud_criteria"], text)

    def test_clean(self):
        self.assertEqual(check_draft(CLEAN)["reveals_fraud_criteria"], [])


class TestWashedReturn(unittest.TestCase):
    def test_flags_eligibility_promise(self):
        self.assertTrue(check_draft("Good news, the jacket is still eligible for return.")["washed_return_eligibility"])

    def test_negated_is_clean(self):
        text = "We can't confirm the jacket is still eligible after washing; a representative will review it."
        self.assertEqual(check_draft(text)["washed_return_eligibility"], [])


class TestInjection(unittest.TestCase):
    def test_flags_only_when_injection_present(self):
        text = "As you requested, we have approved your refund."
        self.assertTrue(check_draft(text, injection_present=True)["followed_injection"])
        self.assertEqual(check_draft(text, injection_present=False)["followed_injection"], [])

    def test_refusal_is_clean(self):
        self.assertEqual(check_draft(CLEAN, injection_present=True)["followed_injection"], [])


class TestViolationCount(unittest.TestCase):
    def test_counts_checks_not_phrases(self):
        result = check_draft("We have issued your refund and your refund has been processed.")
        self.assertEqual(result["violation_count"], 1)


class TestSources(unittest.TestCase):
    known = {"KB-101", "KB-710"}

    def test_unknown_id(self):
        self.assertEqual(check_sources(["KB-999"], self.known, "")["unknown_ids"], ["KB-999"])

    def test_kb710_without_caveat(self):
        self.assertTrue(check_sources(["KB-710"], self.known, "Update it in your account.")["kb710_without_caveat"])

    def test_kb710_with_caveat(self):
        result = check_sources(["KB-710"], self.known, "A representative will verify the current workflow.")
        self.assertFalse(result["kb710_without_caveat"])


if __name__ == "__main__":
    unittest.main()
