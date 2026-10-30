# Metrics: eval_20261030T231525Z_tune_small_v2

Run logs: C:/Users/athav/OneDrive/Documents/Alpine Outdoor/runs/eval_20261030T231525Z_tune_small_v2.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: tune | Mode: fields_only | Prompt versions: v2 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v2 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 20/28 (71%) |
| Route = policy-consistent label | 21/28 (75%) |
| Required approval recall | 8/14 (57%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 15/15 (100%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | n/a |
| KB-710 cited without caveat (v3 onwards) | n/a |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 5/28 |
|   promises_action | 4/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 1/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 6/28 |
|   stop_use_advice | 6/28 |
|   unsourced_safety_instruction | 2/28 |
| Mean latency per call (s) | 6.7 |
| Mean cost per record (USD) | 0.0007 |
| Total cost (USD) | 0.0201 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v2 |
|---|---|
| Account issue | 1/1 (100%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 2/4 (50%) |
| Potential fraud | 1/1 (100%) |
| Product question | 2/4 (50%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 3/5 (60%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: tune | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v2 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v2 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 18/28 (64%) |
| Route = policy-consistent label | 19/28 (68%) |
| Required approval recall | 10/14 (71%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 14/15 (93%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | n/a |
| KB-710 cited without caveat (v3 onwards) | n/a |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 4/28 |
|   promises_action | 3/28 |
|   continue_using | 0/28 |
|   safety_clearance | 1/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 1/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 3/28 |
|   stop_use_advice | 3/28 |
|   unsourced_safety_instruction | 1/28 |
| Mean latency per call (s) | 6.9 |
| Mean cost per record (USD) | 0.0008 |
| Total cost (USD) | 0.0214 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v2 |
|---|---|
| Account issue | 0/1 (0%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 0/1 (0%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 2/4 (50%) |
| Potential fraud | 1/1 (100%) |
| Product question | 1/4 (25%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 4/5 (80%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
