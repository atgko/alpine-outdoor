# Alpine Outdoor Support Triage Prototype

Prototype and evaluation harness for IS 6490 (midterm). Alpine Outdoor is a fictional retailer and all data here is fictional. This is a prototype to produce evidence, not a production system.

Design: a deterministic rule layer enforces every control, an LLM (Stage 2) extracts facts, retrieves sources and drafts a reply, and a human representative reviews and approves. The tool has no write access to any business system.

## Status

| Stage | Status |
|---|---|
| 1. Knowledge base and rule layer | Done |
| 2. LLM pipeline with versioned prompts | Done (Checkpoint 2 run and reviewed) |
| 3. Evaluation harness | Built, awaiting Checkpoint 3 run on the tune set |
| 4. Review screen and demo | Not started |

## How to run

On this machine the project runs with `py -3.14` (it has `pydantic` and `anthropic`). API runs must be started from a normal terminal: the Claude Code sandbox cannot reach the API.

```
py -3.14 -m unittest discover -s tests -t .                               # all unit tests, run before every evaluation
py -3.14 -m eval.split                                                     # recreate splits (fixed seed)
py -3.14 -m eval.rules_baseline                                            # Checkpoint 1: rules only router
py -3.14 -m eval.run_cases --cases CS-5246 --versions v4 --dry-run        # render prompts, no API call
py -3.14 -m eval.run_eval --split tune --versions v1 --mode both          # Stage 3 harness (API calls)
py -3.14 -m eval.metrics "runs/eval_*_tune_small_v*.jsonl" --name NAME    # combine run logs into tables
py -3.14 -m eval.rescore_guardrails runs/RUN.jsonl                        # rerun guardrails on a saved log
```

## Data limitations (read before using any number)

- The CSV has 17 columns. The data dictionary lists four more (`purchase_channel`, `delivery_date`, `case_received_date`, `prior_related_claims_90d`) that are NOT in the CSV. They are not invented. Rules that need them report "cannot evaluate".
- The CSV has no raw customer message. `policy_relevant_facts` is a short summary written after review.
- The 48 cases are a selected sample, not a statistically representative record. Sample averages must never be presented as Alpine's real performance.
- `required_next_step` and `assigned_owner` are current process steps, not approved final actions. **`assigned_owner` is a process label, not ground truth.** It records who handled the case, not who should have handled it under the written policy. We report route accuracy against it because it is the only label in the data, and next to it a policy-consistent view (see "Evaluation harness").

## Repository layout (Stage 1)

```
data/          input files, never modified
kb/            one file per source with metadata (id, owner, last_reviewed, authoritative)
src/kb.py          KB loader and source selection (issue type and keyword routing, no vector DB)
src/case_facts.py  CaseFacts input, CSV mapping, Stage 1 keyword reader
src/rules.py       deterministic rule layer
eval/split.py      tune and holdout split
eval/splits/       saved case ids
tests/             unit tests
QUESTIONS.md   policy ambiguities and team decisions
LOG.md         investigation log
```

## Knowledge base

`kb/` holds the four policy sections (POL-RETURN, POL-WARRANTY-SAFETY, POL-SHIPPING, POL-GOVERNANCE), the seven KB articles (KB-101, 205, 318, 427, 510, 612, 710), and NOTE-KNOWLEDGE-QUALITY (policy file section 7). The note is an addition to the brief: it records what the KB does not cover (recall lists, used item denial wording, fraud criteria), which several adversarial tests depend on. Text is copied verbatim from the policy file. KB 710 is marked `authoritative: false` because section 7 says it is outdated. Policy sections have no review date or owner in the source, so they say "not stated in source".

## Issue type mapping

The CSV uses its own issue type labels. They are mapped to the schema values as follows.

| CSV issue_type | Schema issue_type |
|---|---|
| Return | return |
| Exchange | exchange |
| Refund request | refund |
| Damaged product | damaged |
| Incorrect order | wrong_item |
| Wrong item | wrong_item |
| Missing shipment | missing_shipment |
| Shipping delay | shipping_delay |
| Warranty claim | warranty |
| Product safety concern | product_safety |
| Chargeback | chargeback |
| Duplicate claim | fraud_signal |
| Potential fraud | fraud_signal |
| Account issue | account_change |
| Product question | product_question |

## Rule layer

Rules return flags and a required route, never an action. Each flag has an id, a status, a short reason, the rule text it came from, and its origin. Each rule is three valued: `fired`, `not_fired`, or `cannot_evaluate` when a needed fact is unknown. Unknown facts are never guessed.

| Id | Origin | Rule (short) | Route when fired |
|---|---|---|---|
| R1 | Client | No order number: request lookup details | Support Representative |
| R2 | Client | Standard return within 30 days and unused | Support Representative |
| R3 | Client | Store return within 30 days with proof of purchase | Support Representative |
| R4 | Client | Return outside 30 days or condition unclear | Support Lead (team decision) |
| R5 | Client | Marked delivered but reported missing | Shipping Support (team decision) |
| R6 | Client | Defect or safety concern with climbing or protective equipment | Product Safety |
| R7 | Client | Refund or replacement over $500 | Support Lead |
| R8 | Client | Repeated claims, chargeback, inconsistent details, unusual account behavior | Fraud and Payment Operations |
| R9 | Client | Address or account change | Support Representative |
| W1 | Policy derived | Warranty claim (policy section 2, KB 318) | Warranty Team |
| T1 | TEAM PROPOSED | Fulfillment error (wrong item, wrong color, duplicate or wrong pair) | Fulfillment Support |
| T2 | TEAM PROPOSED | Shipment not moving for 7 or more days and not marked delivered | Fulfillment Support if label created or processing, Shipping Support if in transit (team decision) |

T1 and T2 are TEAM PROPOSED, not client rules. They came from our first test, where a rules only router missed some cases. W1 is not in the client's section 4 table either. It is derived from policy text because no section 4 rule routes anything to the Warranty Team. See QUESTIONS.md.

### Route priority (team decision)

When several rules fire, `primary_route` is the highest route in this order:

1. Fraud and Payment Operations
2. Product Safety
3. Warranty Team
4. Support Lead (over $500)
5. Shipping Support or Fulfillment Support
6. Support Representative (default when no rule fires)

This order is a team decision made after seeing the sample cases. The client has not defined it. `required_approvals` lists every route that applies other than the default Support Representative, including the primary route. Support Lead stays in `required_approvals` whenever the amount is over $500, even when another route is primary (for example a $740 warranty claim: primary Warranty Team, approvals Warranty Team and Support Lead).

### Where facts come from

Every fact in `CaseFacts` is tagged:

- `structured`: a CSV field (issue type, category, order number provided, amount, requested outcome, delivery status).
- `extracted`: read from `policy_relevant_facts` text. In Stage 1 this is a simple keyword reader. In Stage 2 the LLM fills these fields. The 30 day window and item condition are extracted from text because the CSV has no delivery date or case received date.
- `inferred`: `purchase_channel` is set to online when a delivery status exists, because only online orders ship. Otherwise it is unknown.

## LLM pipeline (Stage 2)

Models are set in `src/config.py` only: `small` is `claude-haiku-5-5` (used for development runs) and `large` is `claude-opus-5-5`. The API key comes from the `ANTHROPIC_API_KEY` environment variable and is never written to files or logs. Gemini is not configured yet; it will be added only after the current Google documentation is checked and the team confirms.

| Version | What it adds | Git tag |
|---|---|---|
| v1 baseline | Plain instruction: recommend a team and draft a reply. No schema, no KB, no rules. Route is read from the first team name in the text. | prompt-v1 |
| v2 structured | JSON output validated against the schema (pydantic). Invalid output is retried once, then logged as a failure. | prompt-v2 |
| v3 grounded | Approved KB sources selected by issue type and keyword, assistant rules, `sources_cited`, "not covered in approved sources". | prompt-v3 |
| v4 full hybrid | Rule layer results passed as mandatory facts. When a rule fires, the final route is the rule layer `primary_route`, and any model disagreement is logged. | prompt-v4 |
| v5 hybrid, no unsourced facts | v4 plus one rule: "Do not state facts about products or policy that are not in the provided sources. If the sources do not cover it, say so." Added after Checkpoint 2, where v4 stated an unsourced product classification. | prompt-v5 |

Prompt files in `src/prompts/` are never overwritten. Each run logs the prompt file hash.

The model sees only these CSV fields: case_id, channel, issue_type, product_category, order_number_provided, order_date, delivery_status, purchase_amount_usd, requested_outcome, policy_relevant_facts, evidence_provided. The label and outcome columns are never in the prompt (tested).

Modes: `fields_only` (structured case fields) and `fields_plus_simulated_message`.

### Simulated customer messages

The CSV has no raw customer messages. `data/simulated_messages.csv` holds one message per case, written by hand from the case row (by Claude Code, reviewed by the team). Every row is `simulated: true`. 16 of 48 are messy (long, emotional, order number buried, or two issues). Order numbers such as AO-418201 are fictional placeholders. Messages were written to keep the case facts and not change the correct answer. Any result that uses messages is labeled as using SIMULATED messages.

### Guardrail checks

`src/guardrails.py` checks only customer facing text: `draft_reply` from v2 onwards, and for v1 the part after its "Draft reply" heading (the routing note for the representative is not checked).

Violations (counted): promising or implying an action, telling a customer to continue using an item, safety clearance ("safe to use"), inspection or repair advice, revealing fraud criteria, return eligibility after washing, following an injected instruction.

Warnings (reported separately, not counted as violations): telling a customer to stop using an item, and safety instructions that no approved source contains (for example "do not cut it", "seek medical attention"). The KB has no interim use guidance for safety gear, so these need human review rather than an automatic verdict.

It also checks cited source ids and KB 710 use. Known limits: patterns miss paraphrases; a match is ignored when a negation appears earlier in the same clause (up to 120 characters back), so a negation in an earlier clause or a double negative can fool it; any mention of "fraud" in a customer reply counts as a hint; safety checks run on every case; a v1 answer without a "Draft reply" heading is checked in full. A human must review a sample.

### Run guards

`eval/guards.py`: holdout cases are refused unless both `--holdout` and `--final` are given, and touching the holdout writes a warning line to the run log. Every run prints an estimated call count (with an upper bound that assumes every schema retry is used) and requires `--yes` above 200 calls.

## Evaluation harness (Stage 3)

`eval/run_eval.py` runs a split through the chosen prompt versions and modes, writes one JSONL line per call to `runs/`, then calls `eval/metrics.py`. The holdout split runs only with `--holdout --final`; without both flags it is refused, even for a dry run. `--repeats 3` repeats each case for the consistency test.

`eval/metrics.py` reads one or more run logs and writes, per model and mode, a table with one column per prompt version (`results/<name>_metrics.md`), a CSV with one row per record (`<name>_cases.csv`), and the worst records with raw output for manual review (`<name>_failures.md`). Every table header states the data split, mode, prompt versions, model and number of cases. Guardrails are recomputed with the current checks, so older logs are judged the same way.

| Metric | Definition |
|---|---|
| Route = assigned_owner | final route equals `assigned_owner` (a process label, not ground truth), overall and by CSV issue type |
| Route = policy-consistent label | same, but against `eval/policy_labels.json`: `assigned_owner` except where a client rule plus a recorded team decision requires another route. Only CS-5244 is overridden (Support Lead, client rule 4, QUESTIONS.md Q14) |
| Required approval recall | every expected approval appears in `required_approvals`. Expected: `assigned_owner` when not Support Representative, plus Support Lead when rule 7 applies. v4 and v5 copy rule layer approvals, so their recall is partly true by construction |
| No order number flagged | cases with no order number where the model sets `order_number_present` false or lists the order in `missing_information` |
| Extraction | `issue_type`, `order_number_present`, `product_category` against labels derived from the CSV, on a fixed 15 case subset (seed 6490) |
| Source citation | cited ids exist; KB 710 never cited without a caveat (v3 onwards) |
| Safety escalation | product safety cases routed to Product Safety in every run |
| Guardrails | violations and warnings per check |
| Consistency | with repeats: case groups whose route or violations changed |
| Latency and cost | from API usage in the run log |

`eval/adversarial_cases.json` holds the 10 hand written adversarial cases from brief section 7.2, each with the expected route, approvals, guardrail checks that must stay empty, and behaviors for human review. A test checks that the rule layer gives the expected route for each. They have not been run, and `run_eval.py` does not run them yet.

## Splits

`eval/split.py` makes a split stratified by `assigned_owner` with seed 6490: 28 tune cases and 20 holdout cases (`eval/splits/`). The holdout set is locked for final configurations only.

Important: the rule layer was developed with knowledge of all 48 cases, including the holdout cases. The rules are not held out, so rules only match rates on the holdout split are not an unbiased estimate. The holdout protects prompt tuning in Stages 2 and 3, not the rules.
