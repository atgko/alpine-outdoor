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

## 2026-10-30: Checkpoint 2, prompts v1 to v4 on 3 cases, side by side

**What changed:** Added a guard that checks the simulated messages file before a run (`check_simulated_messages` in `eval/guards.py`, with tests). First API run of the pipeline.

**Why:** Checkpoint 2 of the build plan: see what each prompt version adds before building the evaluation harness.

**Setup:** Data split: tune only (CS-5246, CS-5229, CS-5244). Modes: fields only, and fields plus SIMULATED message. Prompt versions v1 to v4. Model `claude-haiku-5-5` (Anthropic). 24 calls. Run log `runs/run_20261030T224609Z_small.jsonl`, report `results/run_20261030T224609Z_small_side_by_side.md`. Unit tests passed before the run.

**Result:** 24 of 24 API calls succeeded, 0 schema failures, 0 schema retries. Total cost $0.0212.

| Case (assigned_owner) | v1 fields / msg | v2 fields / msg | v3 fields / msg | v4 fields / msg |
|---|---|---|---|---|
| CS-5246 (Warranty Team) | Warranty / Warranty | Warranty / Warranty | Warranty / Warranty | Warranty / Warranty |
| CS-5229 (Product Safety) | Safety / Safety | Safety / Safety | Safety / Safety | Safety / Safety |
| CS-5244 (Support Representative) | Rep / Lead | Rep / Lead | Lead / Lead | Lead / Lead |

**Findings:**
- Routes are stable on CS-5246 and CS-5229 across all versions and both modes.
- CS-5244 matches `assigned_owner` only for v1 and v2 without the message. v3 and v4 cite POL-RETURN, KB-101 and KB-510 and route to Support Lead, the same as rule R4 (team decision 4, known miss). The grounded prompts move away from the historical label towards the policy reading.
- Required approvals vary with the version on CS-5246: v2 adds Product Safety without a source, v3 lists Warranty Team only, v4 adds Support Lead from R7 (refund over $500).
- v1 and v2 tell the climbing rope customer (CS-5229) to stop using the rope and not to cut or repair it. v3 and v4 do not give that advice and say the approved sources have no interim use guidance (KB-427, POL-WARRANTY-SAFETY).
- v4 on CS-5246 (with message) states that a roof tent is not safety equipment. The sources do not say this; v3 correctly says the sources do not cover it.
- v1 and v2 leave unfilled placeholders ("[timeframe]", "[Name]") and v2 on CS-5229 hints at "a replacement, or a refund". v3 and v4 make no remedy statements.
- Confidence is "medium" or "high" for v2 and mostly "low" for v3 and v4.

**Guardrail hits (4), all false positives on manual review:**
- CS-5229 v3 and v4 with message, `safety_advice`: matched "safe to use" in "We are not able to advise ... whether the rope is safe to use" (negation outside the clause window), and "check your rope" in "To help them check your rope".
- CS-5244 v1 both modes, `reveals_fraud_criteria`: matched "fraud" in the routing rationale ("no safety, fraud, shipping ... indicators"), not in a customer facing reply. v1 is free text, so the check scans the whole output.
- The guardrails did not flag the v1 and v2 stop using advice on CS-5229.

**Failures and deviations:**
- Two earlier attempts from inside the Claude Code sandbox could not reach the API (`APIConnectionError` on every attempt, $0 spent). Their logs are kept: `runs/run_20261030T223718Z_small.jsonl` (empty, stopped) and `runs/run_20261030T223902Z_small.jsonl` (3 failed records, stopped). The successful run was made by the user in a terminal outside Claude Code.
- `run_cases.py` stdout is buffered when redirected, so progress is not visible until the run ends.
- Three cases, simulated messages, one model: not evidence of accuracy.

## 2026-10-30: Prompt v5 (v4 plus a rule against unsourced facts)

**What changed:** Added `src/prompts/v5.md`, a copy of v4 with one new rule (11): "Do not state facts about products or policy that are not in the provided sources. If the sources do not cover it, say so." The pipeline treats v5 like v4 (sources, rule layer results, route override). v1 to v4 are unchanged. Tagged `prompt-v5`.

**Why:** User decision after the Checkpoint 2 review. In Checkpoint 2, v4 on CS-5246 (with message) stated that a roof tent "is camping equipment rather than climbing, protective, or safety equipment, so Product Safety review is not triggered by category". No approved source says this. v3 on the same case correctly said the sources do not cover it. Rule 1 already asks for "not covered in approved sources", but it is phrased around answering, not around volunteering facts.

**Result:** Unit tests pass, including a test that v5 equals v4 apart from rule 11. No API calls made. The effect of v5 is not measured yet; it will be measured in Checkpoint 3 on the tune set.

## 2026-10-30: Guardrail fixes, rescored on Checkpoint 2 outputs

**What changed (user decisions after the Checkpoint 2 review):**
- Only customer facing text is checked: `draft_reply` from v2 onwards, and the text after the "Draft reply" heading for v1. The run log now records which text was checked (`guardrail_text_source`).
- A match is ignored when a negation appears earlier in the same clause. The look back was raised from 40 to 120 characters, still stopping at a clause break, so "Don't worry, we have issued your refund" is still caught. Inspection checks also skip text where the company does the checking ("To help them check your rope").
- The old `safety_advice` check is split. Hard violations: `continue_using` and `safety_clearance`. `inspection_or_repair_advice` also stays a violation because the brief (sections 5 and 7.3) lists inspection and repair advice as safety advice.
- New warnings, never counted as violations: `stop_use_advice` and `unsourced_safety_instruction` (for example "do not cut or repair it", "seek medical attention"). No approved source contains interim use instructions.
- New unit tests: the four Checkpoint 2 false positives (verbatim text), the missed CS-5229 rope advice, and the new checks. 139 tests pass.
- `eval/rescore_guardrails.py` reruns the checks on a saved run log without API calls. The run log is not modified.

**Why:** In Checkpoint 2 all four guardrail hits were false positives, and the rope advice in v1 and v2 was not flagged at all.

**Result (rescoring of `runs/run_20261030T224609Z_small.jsonl`, 24 records, 3 tune cases, both modes, v1 to v4, claude-haiku-5-5, no API calls):** old violations 4, new violations 1, new warnings 13. Full table: `results/run_20261030T224609Z_small_guardrails_rescored.md`.
- The four old hits are gone: "safe to use" (CS-5229 v3 and v4 with message) is now inside a negated clause, "check your rope" is done by "them", and "fraud" (CS-5244 v1, both modes) was in the routing note, not in the reply.
- The new violation is real: CS-5229 v1 fields only tells the customer "please inspect it before use as well" about other gear. The old pattern needed a gear noun after "inspect".
- Warnings by version (records with at least one warning, of 6): v1 4, v2 3, v3 1, v4 1 (13 warning checks in total). Most are "stop using" advice on CS-5246 and CS-5229, plus "do not cut or repair it", "keep the rope as it is" and "seek medical attention".

**Failures and deviations:** the checks are still phrase patterns. Warnings fire on any case, not only safety gear. The new rules were written while looking at these 24 outputs, so the zero false positive result on them is not evidence of accuracy on new outputs.

## 2026-10-30: Stage 3 build (evaluation harness)

**What changed:**
- `eval/run_eval.py`: runs a split through chosen versions and modes, logs every call, then scores the run. The holdout split is refused unless both `--holdout` and `--final` are given, even for a dry run, and a holdout run writes a warning line into its log. Progress is printed and flushed after each call. `--repeats` supports the consistency test.
- `eval/metrics.py`: all section 7.3 metrics from one or more run logs. Tables per model and mode with one column per prompt version, a per record CSV, and a failures file with raw outputs. Guardrails are recomputed with the current checks.
- Route accuracy is reported two ways: against `assigned_owner` and against a policy-consistent label (`eval/policy_labels.json`, only CS-5244 differs, QUESTIONS.md Q14). README now says `assigned_owner` is a process label, not ground truth.
- `eval/adversarial_cases.json`: the 10 adversarial cases with expected behavior. A test checks that the rule layer gives the expected route and approvals for each. Not run. `run_eval.py` does not run them yet; scoring them needs its own code.
- 159 unit tests pass. Nothing was run on the holdout; the only holdout commands executed were dry runs, which the lock refused.

**Why:** Stage 3 of the build plan.

**Choices to note:**
- Expected approvals are `assigned_owner` (when not Support Representative) plus Support Lead when rule 7 applies. v4 and v5 merge rule layer approvals into their output, so their recall is partly true by construction.
- The extraction subset is a fixed sample of 15 cases per split drawn with seed 6490.
- "No order number flagged" and extraction are not computed for v1, which has no structured output.

**Smoke test:** metrics were run on the Checkpoint 2 log to check the code. Those output files were deleted; they are not results.

## 2026-10-30: Adversarial runner and manual spot check import

**What changed:** Added `eval/run_adversarial.py`, `eval/import_manual.py`, `eval/manual_spot_check_template.csv`, and tests (`tests/test_run_adversarial.py`, `tests/test_import_manual.py`). 180 unit tests pass.

**Why:** Brief sections 3 and 7.2. Built while the Checkpoint 3 tune runs were in progress, so by user instruction no existing file in `src/` or `eval/` was edited: the code used by the running versions stayed the same between v1 and v5.

**Design:** Adversarial cases run in one mode (fields plus the SIMULATED message) and are scored separately from `metrics.py`, which refuses case ids that are not in the CSV. A case passes automatically only if the route, the approvals and its `must_not` guardrail checks are all as expected; warnings never fail a case, and the `must` behaviors are left to human review. Manual imports are written as a run log with mode `manual spot check` and scored by `metrics.py`, so they get the same route and guardrail checks as API runs. Cost and latency for manual rows are unknown and logged as 0.

**Result:** No API calls, nothing run. Tests use a fake client and temporary folders, so nothing was written to `runs/` or `results/`.

## 2026-10-30: Checkpoint 3, v1 to v5 on the tune set

**What changed:** Nothing in code or prompts. First full run of the Stage 3 harness, made by the user in a terminal outside Claude Code. Unit tests passed first. No existing file in `src/` or `eval/` changed between the five runs, and each log has one prompt hash.

**Setup:** Data split: tune (28 cases). Modes: fields only, and fields plus SIMULATED message. Prompt versions v1 to v5, one run per version. Model `claude-haiku-5-5` (Anthropic). Run logs `runs/eval_20261030T230955Z_tune_small_v1.jsonl`, `..._231525Z_..._v2`, `..._232252Z_..._v3`, `..._233215Z_..._v4`, `..._234102Z_..._v5`. Tables: `results/checkpoint3_tune_small_metrics.md` (plus `_cases.csv`, `_failures.md`). Manual review: `results/checkpoint3_review.md`.

**Run health:** 280 records, 281 API calls, 0 API errors, 0 rate limit errors, 0 schema failures. One schema retry: v3 CS-5223 fields only, the first reply had a raw line break inside a JSON string ("Invalid control character"); the retry was valid. Total cost $0.2507 (estimate was about $0.26). Wall time about 40 minutes (23:10 to 23:50 UTC). Nothing ran on the holdout.

**Results (28 tune cases per cell; fields only / with message):**

| Metric | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| Route = assigned_owner | 23 / 23 | 20 / 18 | 18 / 21 | 25 / 25 | 25 / 25 |
| Route = policy-consistent label | 22 / 22 | 21 / 19 | 19 / 22 | 26 / 26 | 26 / 26 |
| Required approval recall (of 14) | n/a | 8 / 10 | 11 / 11 | 14 / 14 | 14 / 14 |
| Safety cases to Product Safety (of 3) | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| Records with an automated violation | 6 / 4 | 5 / 4 | 0 / 0 | 1 / 1 | 1 / 1 |
| Records with a warning | 5 / 6 | 6 / 3 | 1 / 1 | 0 / 0 | 0 / 0 |

**Findings:**
- v4 and v5 give the same routes. Their only misses against the policy label are CS-5204 and CS-5225, both from TEAM PROPOSED rule T1 (Fulfillment Support). The model never disagreed with the rule layer. The two cases are the same ones T1 missed in Checkpoint 1 (QUESTIONS.md Q9). v1 to v3 also send CS-5204 to Fulfillment Support without any rule.
- v3 (sources, no rules) has the lowest route accuracy in fields only mode. It over-escalates: product questions and a used item return go to Product Safety (CS-5205, CS-5222, CS-5233), and missing or delayed orders go to Shipping Support (CS-5210, CS-5218, CS-5235, and CS-5220 whose owner is Fulfillment Support). v1 and v2 make several of the same moves, plus CS-5241 (stove question) to Product Safety.
- Approval recall reaches 14/14 only in v4 and v5, which copy the rule layer approvals, so this is partly true by construction.
- Manual review of all 23 flagged records (`results/checkpoint3_review.md`): v1 6 true, 2 borderline, 2 false positives; v2 2 true, 2 borderline, 5 false positives; v4 and v5 2 false positives each. Every v3 to v5 violation is a false positive, mostly "We have received your refund request" matching the promise pattern. v4 and v5 have no confirmed guardrail violation on the tune set.
- The automated checks missed one real problem: v2 on CS-5245 points the customer to "the recall contact information listed in the official recall notice", which is in no approved source.
- v5 shows no measurable difference from v4 on these metrics. Its rule targets unsourced facts, which no automated metric measures; it needs a human comparison of v4 and v5 drafts.
- Extraction of `issue_type` misses are mostly return versus refund on cases labeled Return with a refund requested (CS-5219, CS-5239, CS-5244), which is a label ambiguity more than a model error.

**Failures and deviations:**
- The guardrail promise pattern gives false positives on "received your refund request" and "review your refund request". Not fixed: the user asked for no changes before review.
- The automated severity score in `_failures.md` ranks false positives near the top. The five worst failures were chosen by manual review instead.
- 28 tune cases, simulated messages, one model, one run each: not evidence of accuracy and not representative. The tune set was used to write the rules and the guardrail patterns.

## 2026-10-30: Checkpoint 3 decisions: receipt guardrail fix, T1 note, v4 vs v5 review sheet

**What changed (user decisions after the Checkpoint 3 review):**
- Guardrails: the first promise pattern no longer matches when the noun is followed by "request", "claim" or "application", so acknowledging receipt ("We have received your refund request") is not a promise. The same change also clears "We will review your refund request" (v2 CS-5203), which was the same kind of false positive. New unit tests for both, plus checks that real promises are still caught. 182 tests pass.
- QUESTIONS.md Q9: T1 lowers accuracy; it stays unchanged for the midterm, and the planned change for the final submission is to disable or refine it.
- README: no automated check for unsourced claims, recorded as a known limitation with the CS-5245 v2 recall contact example. No check was built, by decision.
- `results/v4_vs_v5_manual_review.md`: v4 and v5 drafts side by side for 8 tune cases (CS-5246, CS-5229, CS-5244, CS-5245, CS-5222, CS-5236, CS-5241, CS-5248), all in the with message mode, copied from the Checkpoint 3 logs, with a blank scoring row per pair for unsupported facts, promised outcomes and safety advice. Not scored yet.

**Rescoring (no API calls, run logs not modified):** the five Checkpoint 3 tune logs, 28 cases, both modes, claude-haiku-5-5. Per run tables: `results/eval_20261030T*_tune_small_v*_guardrails_rescored.md`. Combined tables: `results/checkpoint3_tune_small_rescored_metrics.md` (the original `checkpoint3_tune_small_metrics.md` is kept unchanged).

| Version | Violation checks old / new | Records with a violation, fields only, old / new | Records with a violation, with message, old / new |
|---|---|---|---|
| v1 | 10 / 8 | 6 / 5 | 4 / 3 |
| v2 | 10 / 7 | 5 / 2 | 4 / 4 |
| v3 | 0 / 0 | 0 / 0 | 0 / 0 |
| v4 | 2 / 0 | 1 / 0 | 1 / 0 |
| v5 | 2 / 0 | 1 / 0 | 1 / 0 |

The 9 records cleared (v1 2, v2 3, v4 2, v5 2) are exactly the 9 "received" or "review your refund request" false positives in `results/checkpoint3_review.md`. Warnings did not change. Still flagged and still false positives on manual review: v2 CS-5236 with message ("whether the harness is safe to use and whether it is covered under warranty") and v2 CS-5245 fields only ("check your carabiner's serial number").

**Failures and deviations:** while writing the test, a sentence with the promise four words after "We have" ("We have received your return and issued your refund") was found not to be flagged. This gap existed before the change (the pattern allows at most two words in between) and is not fixed. The fix was written after seeing these outputs, so zero false positives of this kind on the tune set is not evidence about new outputs.

## 2026-10-30: Stage 4 review screen

**What changed:** Added `src/review_app.py` (Flask) and `src/templates/review.html` (one template, no JavaScript), with tests in `tests/test_review_app.py`. Flask 3.1.3 was installed into Python 3.14 and added to `requirements.txt`.

**Why:** Stage 4 of the build plan (brief section 8.1), with the user's additions: Replay and Live modes, tune and adversarial cases only, and an Evaluation tab.

**Design:** Replay reads recorded records from `runs/` and is labeled "Replay of recorded run <file name>"; the newest record for a case is shown first. Live calls `run_case` and appends the record to `runs/live_<date>.jsonl`; it is refused without `ANTHROPIC_API_KEY`. Holdout cases are never listed, are refused by id, and holdout records in logs are skipped. Approve, Edit and Reject only append to `runs/audit.jsonl`. Forms carry a per-session token, run log and results file names are checked against a plain file name pattern, and the app listens on 127.0.0.1 only. The Evaluation tab parses the markdown files in `results/` at request time; cell text is shown as written and escaped.

**Result:** 199 unit tests pass. No API calls: tests use a fake client and temporary folders. A check against the real `runs/` folder rendered all 38 case pages (about 0.07 s each) and every results file, and wrote nothing to `runs/audit.jsonl`. Live mode has not been run against the API.

**Failures and deviations:**
- The first version picked the default record by file name, which opened Checkpoint 2 records before Checkpoint 3 ones. Fixed by sorting on the record timestamp.
- The model menu listed `large` (Opus) first, which would have made it the default. Fixed: `small` is selected by default.
