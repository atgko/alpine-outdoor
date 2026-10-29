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

## 2026-10-28: Checkpoint 1, rules only router vs assigned_owner

**What changed:** Added `eval/rules_baseline.py`. It runs the rule layer on all 48 cases under five rule sets and compares `primary_route` with `assigned_owner`. Unit tests (79) were run first and passed.

**Why:** Reproduce the team's earlier rules only baseline (reported as 40 of 48) and measure the effect of each proposed addition separately.

**Setup:** Data split all 48 (tune 28, holdout 20). Mode: structured fields plus keyword extraction from `policy_relevant_facts`, no customer message, no LLM. Run log `runs/rules_baseline_20261029T024611Z.jsonl`. Results in `results/rules_baseline.md` and `results/rules_baseline_cases.csv`.

**Result (match with assigned_owner):**

| Config | All 48 | Tune 28 | Holdout 20 |
|---|---|---|---|
| 9 client rules only | 39/48 | 22/28 | 17/20 |
| Client rules + W1 (without team proposed) | 43/48 | 24/28 | 19/20 |
| + T1 only | 42/48 | 23/28 | 19/20 |
| + T2 only | 45/48 | 26/28 | 19/20 |
| Client rules + W1 + T1 + T2 (with team proposed) | 44/48 | 25/28 | 19/20 |

**Findings:**
- The client rules alone give 39/48, not the 40/48 from the earlier test. The earlier test's exact rule reading is not available, so the one case difference cannot be traced.
- W1 (warranty claims to Warranty Team) fixes 4 cases. It is policy derived, not a client rule.
- T2 (stalled shipment) fixes CS-5220 and CS-5243 and breaks nothing.
- T1 (fulfillment error) fixes CS-5214 and CS-5223 but breaks CS-5204, CS-5225 and CS-5237. Net effect is minus 1 case. It was not tuned to fit (team decision 2).
- CS-5244 (washed jacket) is a known miss under team decision 4.
- Rule 8 is "cannot evaluate" on 45 of 48 cases because `prior_related_claims_90d` is not in the CSV.

**Caveats:** 48 selected cases, not representative. The rules were developed with knowledge of all 48 cases, so the holdout numbers are not an unbiased estimate. The holdout was touched at user request and the run log carries a warning line.

## 2026-10-28: Stage 2 build (prompts v1 to v4, pipeline, guardrails, simulated messages)

**What changed:** Added `src/config.py` (model names in one place), `src/schema.py` (pydantic schema), `src/llm.py` (Anthropic wrapper with counted retries and backoff, SDK retries off), `src/pipeline.py` (one case end to end), `src/guardrails.py` (phrase checks), prompts v1 to v4, `eval/guards.py` (holdout lock and spend guard), `eval/run_cases.py` (side by side runner with `--dry-run`), and `data/simulated_messages.csv` (48 hand written messages, 16 messy, all marked simulated). Resolved Q7 (W1 confirmed as policy derived).

**Why:** Stage 2 of the build plan. Each prompt version adds one thing so its effect can be measured.

**Design choices:** JSON is requested in the prompt and validated with pydantic rather than enforced with the API structured output feature, so that schema failures can be measured and the same check works for other providers. The server side refusal fallback feature is not enabled because it would silently swap the model and contaminate model comparisons; refusals are logged as failures instead. v4 runs the rule layer on structured fields plus keyword extracted facts before the model call; it does not re run rules on model extracted facts.

**Result:** 118 unit tests pass. No API calls made yet.

**Failures and deviations:**
- The `anthropic` SDK is not installed and pip cannot reach PyPI from the Claude Code sandbox (SSL certificate error). The user needs to install it.
- A guardrail test failed on first run: the 25 character negation window cut off "can't" in "We can't confirm the jacket is still eligible". Fixed by checking negation within the same clause up to 40 characters, and added a test that "Don't worry, we have issued your refund" is still caught.
- Three Stage 4 demo cases (CS-5201, CS-5208, CS-5209) are in the holdout split. To be resolved before Stage 4.
