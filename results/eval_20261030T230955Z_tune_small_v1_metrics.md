# Metrics: eval_20261030T230955Z_tune_small_v1

Run logs: C:/Users/athav/OneDrive/Documents/Alpine Outdoor/runs/eval_20261030T230955Z_tune_small_v1.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: tune | Mode: fields_only | Prompt versions: v1 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v1 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | n/a |
| Route = assigned_owner | 23/28 (82%) |
| Route = policy-consistent label | 22/28 (79%) |
| Required approval recall | n/a |
| No order number flagged | n/a |
| Extraction: issue_type (15 case subset) | n/a |
| Extraction: order_number_present | n/a |
| Extraction: product_category | n/a |
| Cited ids unknown (v3 onwards) | n/a |
| KB-710 cited without caveat (v3 onwards) | n/a |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 6/28 |
|   promises_action | 6/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 5/28 |
|   stop_use_advice | 5/28 |
|   unsourced_safety_instruction | 1/28 |
| Mean latency per call (s) | 4.8 |
| Mean cost per record (USD) | 0.0004 |
| Total cost (USD) | 0.0121 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v1 |
|---|---|
| Account issue | 1/1 (100%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 0/1 (0%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 4/4 (100%) |
| Potential fraud | 1/1 (100%) |
| Product question | 3/4 (75%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 4/5 (80%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: tune | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v1 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v1 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | n/a |
| Route = assigned_owner | 23/28 (82%) |
| Route = policy-consistent label | 22/28 (79%) |
| Required approval recall | n/a |
| No order number flagged | n/a |
| Extraction: issue_type (15 case subset) | n/a |
| Extraction: order_number_present | n/a |
| Extraction: product_category | n/a |
| Cited ids unknown (v3 onwards) | n/a |
| KB-710 cited without caveat (v3 onwards) | n/a |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 4/28 |
|   promises_action | 4/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 6/28 |
|   stop_use_advice | 4/28 |
|   unsourced_safety_instruction | 4/28 |
| Mean latency per call (s) | 4.6 |
| Mean cost per record (USD) | 0.0004 |
| Total cost (USD) | 0.0118 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v1 |
|---|---|
| Account issue | 0/1 (0%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 2/4 (50%) |
| Potential fraud | 1/1 (100%) |
| Product question | 4/4 (100%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 5/5 (100%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
