# Project Status and Handoff

Last updated: 2026-10-31. Read this first when resuming. The full brief is `claude_code_build_prompt.md`; section 10 (rules for how we work) applies to the whole project.

## Where we are

| Stage | State |
|---|---|
| Stage 1: knowledge base and rule layer | Done, committed |
| Checkpoint 1: rules only baseline | Done, committed |
| Stage 2: LLM pipeline, prompts v1 to v5 | Done. v5 added after Checkpoint 2 review |
| Checkpoint 2: v1 to v4 on 3 cases, side by side | Done and reviewed 2026-10-30 |
| Stage 3: evaluation harness | Built and committed 2026-10-30 (`run_eval.py`, `metrics.py`, adversarial cases, guardrail fixes) |
| Checkpoint 3: v1 to v5 on the tune set | Run and reviewed 2026-10-30. Decisions applied. v4 vs v5 sheet scored 2026-10-31: v5 is the final configuration, chosen as a tie-break |
| Stage 4: review screen and demo | Review screen built 2026-10-30 (`src/review_app.py`, Replay and Live, audit log, Evaluation tab). Live mode not yet run. Demo script (`demo.py`, `DEMO.md`) not started |
| Final evaluation (section 9) | Adversarial set and holdout run and reviewed 2026-10-31 (70 calls, $0.0732). The holdout is used up. Consistency test and `results/summary.md` not done |

Repository: private GitHub repo https://github.com/atgko/alpine-outdoor (remote `origin`, branch `main`). Tags `prompt-v1` to `prompt-v5` are pushed.

## Outstanding actions (user)

1. Read the v5 drafts for CS-5208 and CS-5217 and the ADV-09 outputs (LOG.md entry of 2026-10-31 has the findings).
2. Try the review screen: `py -3.14 -m src.review_app` in a normal terminal, open http://127.0.0.1:5000. Replay works without the key; Live mode makes real API calls and logs them to `runs/live_<date>.jsonl`. Flask 3.1.3 was installed into Python 3.14 on 2026-10-30.
2. API key is set and works. The user accepted the risk of keeping the key pasted on 2026-10-28 active until the project ends, and will revoke it then. Never paste keys into chat or files.
3. API runs cannot reach the network from the Claude Code sandbox, including `!` commands. The user runs them in a normal terminal outside Claude Code.

## Approved on 2026-10-30

- Checkpoint 2 run on `claude-haiku-5-5`: 24 calls expected, 42 at most. `claude-opus-5-5` is not used yet.
- Push to origin after each stage and checkpoint commit.
- The five simulated messages shown for review.
- JSON validation after the reply stays, and refusal fallback stays off.

## Python interpreter

`python` on PATH is the `hermes-agent` venv (3.11), which has no `anthropic` and belongs to another tool. Do not install into it. `pip` installs into Python 3.14, so run the project with `py -3.14`.

## Outstanding decisions (before later stages)

- **Demo cases in the holdout: resolved 2026-10-30.** The user chose to replace the holdout demo cases with tune cases. Stage 4 order: CS-5219 (clean return, replaces CS-5201), CS-5227 (no order number), CS-5242 ($1,200 refund, replaces CS-5209), CS-5229 (rope sheath abrasion, replaces CS-5208), CS-5244 (washed jacket, KB 510). This overrides the list in section 8.2 of the brief.
- **Gemini.** Not configured. Before Stage 3, check the current Google docs for model names and free tier limits, report them, and get confirmation before any Gemini call. The Gemini SDK must also be installed by the user.
- **Refusal fallback is off, confirmed by the user 2026-10-30.** It would silently swap the model and mix models in comparisons. Refusals are logged as failures.

## Final evaluation (go given 2026-10-31)

Final configuration: prompt v5, `claude-haiku-5-5`, chosen as a tie-break (scored sheet: v4 = 3, v5 = 2 across 8 tune cases; the only clear difference is CS-5244, and with one run per case it could be run to run variation).

Limits set by the user:

1. Adversarial set on v1, v3 and v5 on the small model.
2. Holdout once on v5, small model, both modes, with `--holdout --final`.
3. Rule T1 stays as is, as decided for the midterm.
4. No changes to prompts, rules or guardrails after the holdout run, and no second holdout run.

Results: holdout v5 (20 cases per mode, fields only / with message): route 19/20 / 19/20 against both labels, approval recall 10/10 / 10/10, no order number flagged 1/1 / 1/1, violations 0 / 0, warnings 0 / 1, $0.0440. Adversarial automated pass of 10: v1 5, v3 8, v5 9; the v5 failure (ADV-07 `safety_clearance`) is a false positive on manual review. The holdout tests the prompts, not the rules, which were written knowing all 48 cases. Do not run it again.

Commands as run by the user (for the record, do not rerun the last line):

```
cd "C:\Users\athav\OneDrive\Documents\Alpine Outdoor"
py -3.14 -m unittest discover -s tests -t .
py -3.14 -m eval.run_adversarial --versions v1 v3 v5 --model small --dry-run
py -3.14 -m eval.run_eval --split holdout --versions v5 --mode both --model small --holdout --final --dry-run
py -3.14 -m eval.run_adversarial --versions v1 v3 v5 --model small
py -3.14 -m eval.run_eval --split holdout --versions v5 --mode both --model small --holdout --final
```

Estimate: adversarial 10 cases x 3 versions = 30 calls (up to 50), about $0.03 (up to $0.05). Holdout 20 cases x 2 modes = 40 calls (up to 80), about $0.04 (up to $0.09). Total 70 calls (up to 130), about $0.07 (up to $0.14), about 12 minutes. Costs use the per call averages in the Checkpoint 3 tune logs, so treat as rough. Each command stays under the 200 call guard, so no `--yes` is needed.

Not in this go: the consistency test (brief section 9 item 3), the adversarial set on v2 and v4 (item 2), other providers (item 1), and `results/summary.md` (item 4).

## Checkpoint 3 commands (done, kept for reference)

```
cd "C:\Users\athav\OneDrive\Documents\Alpine Outdoor"
py -3.14 -m unittest discover -s tests -t .
py -3.14 -m eval.run_eval --split tune --versions v1 --mode both --model small
py -3.14 -m eval.run_eval --split tune --versions v2 --mode both --model small
py -3.14 -m eval.run_eval --split tune --versions v3 --mode both --model small
py -3.14 -m eval.run_eval --split tune --versions v4 --mode both --model small
py -3.14 -m eval.run_eval --split tune --versions v5 --mode both --model small
py -3.14 -m eval.metrics "runs/eval_*_tune_small_v*.jsonl" --name checkpoint3_tune_small
```

Estimate: 28 tune cases x 2 modes = 56 calls per version, 280 in total (up to 504 if every v2 to v5 call needs its schema retry). About $0.26 expected, $0.60 at most, about 40 minutes. Based on per call costs in the Checkpoint 2 log (3 cases), so treat as rough. Each command stays under the 200 call guard, so no `--yes` is needed. If a version is rerun, delete or exclude the failed log before the metrics command, because the wildcard picks up every matching log.

## Next steps once unblocked

1. Checkpoint 3 is done (280 records, 281 calls, $0.2507, 0 failures, 1 schema retry) and reviewed. Decisions of 2026-10-30 are applied: receipt false positive fixed and the five tune logs rescored (v4 and v5 now 0 violations), T1 unchanged for the midterm (Q9), no unsourced-claims check (README known limitation), v4 vs v5 review sheet created and scored.
2. Known guardrail limits, not fixed: false positives on v2 CS-5236 with message and v2 CS-5245 fields only; a promise more than two words after "we have" is missed; the stop use style line in v4 and v5 CS-5236 ("not to rely on the harness") found in manual scoring raised no warning.
3. Next: wait for the user. Remaining from brief section 9, not part of this go: consistency test, adversarial set on v2 and v4, other providers, `results/summary.md`.
4. T1: the holdout ran with T1 as written (QUESTIONS.md Q9). Any later T1 change cannot be checked on the holdout (limit 4), and any such result must be reported as tune only.
5. Prompts, rules and guardrails are frozen from now on. Built, not run: `eval/import_manual.py` (manual spot check) needs the user to paste chat outputs into the template CSV.

## Key results so far (from logged runs only)

Checkpoint 1, rules only router vs `assigned_owner`, all 48 cases, structured fields plus keyword extraction, no LLM (run log `runs/rules_baseline_20261029T024611Z.jsonl`):

| Rule set | All 48 | Tune 28 | Holdout 20 |
|---|---|---|---|
| 9 client rules only | 39/48 | 22/28 | 17/20 |
| Client rules + W1 (without team proposed) | 43/48 | 24/28 | 19/20 |
| Client rules + W1 + T1 + T2 (with team proposed) | 44/48 | 25/28 | 19/20 |

T2 (stalled shipment) helps by 2 cases. T1 (fulfillment error) is net minus 1. The earlier team test reported 40/48 for client rules; we got 39/48 and the one case difference cannot be traced. The rules were developed with knowledge of all 48 cases, so holdout numbers are not an unbiased estimate.

Checkpoint 2 (`runs/run_20261030T224609Z_small.jsonl`, 3 tune cases, both modes, v1 to v4, claude-haiku-5-5): 24/24 API ok, 0 schema failures, $0.0212. Guardrails rescored offline after the fixes: violations 4 to 1, warnings 13.

## Decisions on 2026-10-30 (after Checkpoint 2 review)

- Prompt v5 = v4 plus the rule against unsourced facts. v1 to v4 unchanged.
- Guardrails check only customer facing text and ignore matches inside a negation. Continue using and safety clearance are hard violations. Stop use advice and unsourced safety instructions are warnings, not violations.
- Route accuracy is reported against `assigned_owner` and against a policy-consistent label (only CS-5244 differs, QUESTIONS.md Q14).
- Nothing runs on the holdout until the final evaluation.

## Decisions already made (see QUESTIONS.md for detail)

- Route priority: Fraud and Payment Operations, Product Safety, Warranty Team, Support Lead, Shipping or Fulfillment Support, Support Representative. Team decision, not a client rule. Support Lead stays in `required_approvals` when over $500.
- W1 (warranty claims to Warranty Team) kept as policy derived (policy section 2 and KB 318), separate from the nine client rules.
- T1 and T2 are TEAM PROPOSED. T1 is kept as written and not tuned to fit.
- Rule 4 routes to Support Lead. CS-5244 is a known miss.
- T2 tie break: label created or processing to Fulfillment Support, in transit to Shipping Support.
- CS-5213 is not routed to Fraud.
- Split: seed 6490, 28 tune and 20 holdout, stratified by `assigned_owner`. Holdout locked in code (`--holdout --final`).

## Environment notes

- Run with `py -3.14`, which has `pydantic` and `anthropic`. See "Python interpreter" above.
- Tests use the standard library `unittest` because pytest could not be installed.
- `.gitattributes` is `* text=auto eol=lf`.
- Do not use em dashes in README or log text.

## Commit history

| Commit | Message |
|---|---|
| 7d1ed22 | chore: initial project files and input data |
| a2e29c0 | Stage 1: rule layer and tests |
| 78a53e9 | Checkpoint 1: rules only baseline |
| 6e9d41c | chore: resolve Q7 (W1 policy derived) and force LF line endings |
| e83a868 to 2e4e47a | prompt v1 to v4, tagged prompt-v1 to prompt-v4 |
| 17f7a8b | Stage 2: LLM pipeline, guardrails and simulated messages |
| 90c2b41 | Checkpoint 2: prompts v1 to v4 on 3 tune cases, side by side |
| 717b764 | prompt v5, tagged prompt-v5 |
| a6b05bf, ff16d5f | fix: guardrail fixes and offline rescoring; Stage 3: evaluation harness |
| 620c999 | feat: adversarial runner and manual spot check import |
| bbb9c6d | Checkpoint 3: v1 to v5 on the tune set |
| 5d204f7 | fix: receipt is not a promise; Checkpoint 3 decisions |
| bff638e | Stage 4: review screen |
| 2233c79 | v4 vs v5 sheet scored by the user (GitHub web edit) |
| b6cf048 | Final configuration and go recorded |
| (next) | Final evaluation: adversarial set and holdout, reviewed (see git log) |
