# Metrics: eval_20261030T234102Z_tune_small_v5

Run logs: C:/Users/athav/OneDrive/Documents/Alpine Outdoor/runs/eval_20261030T234102Z_tune_small_v5.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: tune | Mode: fields_only | Prompt versions: v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v5 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 25/28 (89%) |
| Route = policy-consistent label | 26/28 (93%) |
| Required approval recall | 14/14 (100%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 12/15 (80%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/28 |
| KB-710 cited without caveat (v3 onwards) | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | 0/28 |
| Records with a guardrail violation | 1/28 |
|   promises_action | 1/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 0/28 |
|   stop_use_advice | 0/28 |
|   unsourced_safety_instruction | 0/28 |
| Mean latency per call (s) | 8.5 |
| Mean cost per record (USD) | 0.0011 |
| Total cost (USD) | 0.0303 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v5 |
|---|---|
| Account issue | 1/1 (100%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 4/4 (100%) |
| Potential fraud | 1/1 (100%) |
| Product question | 4/4 (100%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 1/2 (50%) |
| Return | 4/5 (80%) |
| Shipping delay | 1/1 (100%) |
| Warranty claim | 3/3 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: tune | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v5 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 25/28 (89%) |
| Route = policy-consistent label | 26/28 (93%) |
| Required approval recall | 14/14 (100%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 15/15 (100%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/28 |
| KB-710 cited without caveat (v3 onwards) | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | 0/28 |
| Records with a guardrail violation | 1/28 |
|   promises_action | 1/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 0/28 |
|   stop_use_advice | 0/28 |
|   unsourced_safety_instruction | 0/28 |
| Mean latency per call (s) | 8.6 |
| Mean cost per record (USD) | 0.0011 |
| Total cost (USD) | 0.0314 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v5 |
|---|---|
| Account issue | 1/1 (100%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 4/4 (100%) |
| Potential fraud | 1/1 (100%) |
| Product question | 4/4 (100%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 1/2 (50%) |
| Return | 4/5 (80%) |
| Shipping delay | 1/1 (100%) |
| Warranty claim | 3/3 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
