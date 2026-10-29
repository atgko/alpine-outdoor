# Project Status and Handoff

Last updated: 2026-10-28. Read this first when resuming. The full brief is `claude_code_build_prompt.md`; section 10 (rules for how we work) applies to the whole project.

## Where we are

| Stage | State |
|---|---|
| Stage 1: knowledge base and rule layer | Done, committed |
| Checkpoint 1: rules only baseline | Done, committed |
| Stage 2: LLM pipeline, prompts v1 to v4 | Built and committed. No API call made yet |
| Checkpoint 2: v1 to v4 on 3 cases, side by side | NOT RUN. Waiting on the actions below |
| Stage 3: evaluation harness | Not started |
| Stage 4: review screen and demo | Not started |
| Final evaluation (section 9) | Not started. Only after an explicit "go" |

Repository: private GitHub repo https://github.com/atgko/alpine-outdoor (remote `origin`, branch `main`). Tags `prompt-v1` to `prompt-v4` are pushed.

## Outstanding actions (user)

1. Install the SDK: `! pip install anthropic`. The Claude Code sandbox cannot reach PyPI (SSL certificate error), so this must be run by the user.
2. Rotate the Anthropic API key. The key pasted in chat on 2026-10-28 is in the transcript and should be revoked. It also has an unusual prefix (`sk-ant-usr-`), so it may not be a valid API key. Create a new key in the Anthropic Console.
3. Set the new key outside the chat: `setx ANTHROPIC_API_KEY "<new key>"`, then restart Claude Code. Never paste keys into chat or files.
4. Approve the model names: `claude-haiku-5-5` (small, used for development) and `claude-opus-5-5` (large, for comparison). Both are set in `src/config.py`.
5. Approve the Checkpoint 2 run: 24 calls expected, 42 at most, estimated under $0.10 on Haiku (an estimate, not a measurement).
6. Review the 5 example simulated messages (CS-5203, CS-5213, CS-5236, CS-5244, CS-5246) and approve `data/simulated_messages.csv` or request changes.
7. Decide whether Claude should push to GitHub after each stage and checkpoint commit, or only commit locally.

## Outstanding decisions (before later stages)

- **Demo cases in the holdout.** Three of the five Stage 4 demo cases (CS-5201, CS-5208, CS-5209) are in the locked holdout split. Options: swap them for similar tune cases, or accept that the demo touches the holdout and log it.
- **Gemini.** Not configured. Before Stage 3, check the current Google docs for model names and free tier limits, report them, and get confirmation before any Gemini call. The Gemini SDK must also be installed by the user.
- **Refusal fallback is off.** It would silently swap the model and mix models in comparisons. Refusals are logged as failures. The user may ask to turn it on.

## Next steps once unblocked

1. Run the unit tests: `python -m unittest discover -s tests -t .` (118 tests, all passing as of the last commit).
2. Run Checkpoint 2:
   `python -m eval.run_cases --cases CS-5246 CS-5229 CS-5244 --versions v1 v2 v3 v4 --mode both --model small`
   (add `--dry-run` first to see the prompts without any API call). If the sandbox cannot reach the API, the user runs it with `!`.
3. Show the side by side report (`results/run_*_side_by_side.md`), append a LOG.md entry, commit "Checkpoint 2: ...", and stop for review.
4. If prompts change after review, create new versions. Never overwrite a prompt file. Tag each new version.
5. Then Stage 3: `eval/run_eval.py`, `eval/metrics.py`, `eval/adversarial_cases.json`, `eval/import_manual.py`, consistency test. Run v1 to v4 on the tune set only (Checkpoint 3).

## Key results so far (from logged runs only)

Checkpoint 1, rules only router vs `assigned_owner`, all 48 cases, structured fields plus keyword extraction, no LLM (run log `runs/rules_baseline_20261029T024611Z.jsonl`):

| Rule set | All 48 | Tune 28 | Holdout 20 |
|---|---|---|---|
| 9 client rules only | 39/48 | 22/28 | 17/20 |
| Client rules + W1 (without team proposed) | 43/48 | 24/28 | 19/20 |
| Client rules + W1 + T1 + T2 (with team proposed) | 44/48 | 25/28 | 19/20 |

T2 (stalled shipment) helps by 2 cases. T1 (fulfillment error) is net minus 1. The earlier team test reported 40/48 for client rules; we got 39/48 and the one case difference cannot be traced. The rules were developed with knowledge of all 48 cases, so holdout numbers are not an unbiased estimate.

## Decisions already made (see QUESTIONS.md for detail)

- Route priority: Fraud and Payment Operations, Product Safety, Warranty Team, Support Lead, Shipping or Fulfillment Support, Support Representative. Team decision, not a client rule. Support Lead stays in `required_approvals` when over $500.
- W1 (warranty claims to Warranty Team) kept as policy derived (policy section 2 and KB 318), separate from the nine client rules.
- T1 and T2 are TEAM PROPOSED. T1 is kept as written and not tuned to fit.
- Rule 4 routes to Support Lead. CS-5244 is a known miss.
- T2 tie break: label created or processing to Fulfillment Support, in transit to Shipping Support.
- CS-5213 is not routed to Fraud.
- Split: seed 6490, 28 tune and 20 holdout, stratified by `assigned_owner`. Holdout locked in code (`--holdout --final`).

## Environment notes

- Python 3.11. `pydantic` is installed; `anthropic` and `pandas` are not.
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
