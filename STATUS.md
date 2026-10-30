# Project Status and Handoff

Last updated: 2026-10-30. Read this first when resuming. The full brief is `claude_code_build_prompt.md`; section 10 (rules for how we work) applies to the whole project.

## Where we are

| Stage | State |
|---|---|
| Stage 1: knowledge base and rule layer | Done, committed |
| Checkpoint 1: rules only baseline | Done, committed |
| Stage 2: LLM pipeline, prompts v1 to v5 | Done. v5 added after Checkpoint 2 review |
| Checkpoint 2: v1 to v4 on 3 cases, side by side | Done and reviewed 2026-10-30 |
| Stage 3: evaluation harness | Built and committed 2026-10-30 (`run_eval.py`, `metrics.py`, adversarial cases, guardrail fixes) |
| Checkpoint 3: v1 to v5 on the tune set | NOT RUN. Waiting for the user to run the commands below |
| Stage 4: review screen and demo | Not started |
| Final evaluation (section 9) | Not started. Only after an explicit "go" |

Repository: private GitHub repo https://github.com/atgko/alpine-outdoor (remote `origin`, branch `main`). Tags `prompt-v1` to `prompt-v5` are pushed.

## Outstanding actions (user)

1. Run Checkpoint 3 in a normal terminal (commands below), then tell Claude Code the file names printed at the end.
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

## Checkpoint 3 commands (user runs them in a normal terminal)

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

1. After Checkpoint 3 runs: show the metrics tables (`results/checkpoint3_tune_small_metrics.md`) and the five worst failures with raw outputs (from `_failures.md`), append a LOG.md entry, commit "Checkpoint 3: ...", push, and stop for review.
2. If prompts change after review, create new versions. Never overwrite a prompt file. Tag each new version.
3. Not built yet: `eval/import_manual.py` (manual spot check import, brief section 3), adversarial case runner and scoring in `run_eval.py`/`metrics.py`. The adversarial set and the consistency test (`--repeats 3` on 10 cases) belong to the final evaluation, which needs an explicit "go".

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
| after 717b764 | fix: guardrail fixes and offline rescoring; Stage 3: evaluation harness (see git log) |
