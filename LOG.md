# Investigation Log

One entry per experiment or build step: what changed, why, result, and anything that failed.

## 2026-10-28: Stage 1 build (knowledge base and rule layer)

**What changed:** Split the policy file into 12 KB files under `kb/` (4 policy sections, 7 KB articles, 1 knowledge quality note) with owner, review date and authority metadata. Built `src/rules.py` with the 9 client rules, 2 TEAM PROPOSED rules (T1 fulfillment error, T2 stalled shipment) and 1 policy derived rule (W1 warranty). Built `src/case_facts.py` with a keyword reader for text facts. Created the tune (28) and holdout (20) split with seed 6490, stratified by `assigned_owner`.

**Why:** Stage 1 of the build plan. The rule layer must enforce controls independently of any model.

**Team decisions applied:** route priority (Fraud, Product Safety, Warranty, Support Lead, Shipping or Fulfillment, Representative), rule 4 goes to Support Lead, T2 tie break by delivery status, CS-5213 not routed to Fraud. All recorded in QUESTIONS.md.

**Result:** 79 unit tests pass (`python -m unittest discover -s tests -t .`). Every rule has a fired and a not fired test, and a cannot evaluate test where a fact can be unknown. One test checks that the client rule text matches the policy file word for word.

**Failures and deviations:**
- `pip install pytest` failed with an SSL certificate error in this environment, so the tests use the standard library `unittest`. pytest can still run them.
- No section 4 client rule routes to the Warranty Team. W1 was added from policy text and is reported separately (QUESTIONS.md Q7).
- The rules were written with knowledge of all 48 cases, so the holdout split does not hold out the rules.
