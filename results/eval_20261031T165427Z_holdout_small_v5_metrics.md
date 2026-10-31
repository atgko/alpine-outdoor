# Metrics: eval_20261031T165427Z_holdout_small_v5

Run logs: C:/Users/athav/OneDrive/Documents/Alpine Outdoor/runs/eval_20261031T165427Z_holdout_small_v5.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: holdout | Mode: fields_only | Prompt versions: v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 20 | Records: 20

| Metric | v5 |
|---|---|
| API ok | 20/20 (100%) |
| Schema valid (v2 onwards) | 20/20 (100%) |
| Route = assigned_owner | 19/20 (95%) |
| Route = policy-consistent label | 19/20 (95%) |
| Required approval recall | 10/10 (100%) |
| No order number flagged | 1/1 (100%) |
| Extraction: issue_type (15 case subset) | 10/15 (67%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/20 |
| KB-710 cited without caveat (v3 onwards) | 0/20 |
| Safety cases routed to Product Safety | 2/2 (100%) |
| Model disagreed with rules (v4, v5) | 0/20 |
| Records with a guardrail violation | 0/20 |
|   promises_action | 0/20 |
|   continue_using | 0/20 |
|   safety_clearance | 0/20 |
|   inspection_or_repair_advice | 0/20 |
|   reveals_fraud_criteria | 0/20 |
|   washed_return_eligibility | 0/20 |
|   followed_injection | 0/20 |
| Records with a warning (not a violation) | 0/20 |
|   stop_use_advice | 0/20 |
|   unsourced_safety_instruction | 0/20 |
| Mean latency per call (s) | 8.5 |
| Mean cost per record (USD) | 0.0011 |
| Total cost (USD) | 0.0217 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v5 |
|---|---|
| Account issue | 1/1 (100%) |
| Damaged product | 3/3 (100%) |
| Duplicate claim | 1/1 (100%) |
| Exchange | 2/2 (100%) |
| Incorrect order | 0/1 (0%) |
| Missing shipment | 1/1 (100%) |
| Product question | 1/1 (100%) |
| Refund request | 2/2 (100%) |
| Return | 4/4 (100%) |
| Shipping delay | 1/1 (100%) |
| Warranty claim | 2/2 (100%) |
| Wrong item | 1/1 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: holdout | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 20 | Records: 20

| Metric | v5 |
|---|---|
| API ok | 20/20 (100%) |
| Schema valid (v2 onwards) | 20/20 (100%) |
| Route = assigned_owner | 19/20 (95%) |
| Route = policy-consistent label | 19/20 (95%) |
| Required approval recall | 10/10 (100%) |
| No order number flagged | 1/1 (100%) |
| Extraction: issue_type (15 case subset) | 12/15 (80%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/20 |
| KB-710 cited without caveat (v3 onwards) | 0/20 |
| Safety cases routed to Product Safety | 2/2 (100%) |
| Model disagreed with rules (v4, v5) | 0/20 |
| Records with a guardrail violation | 0/20 |
|   promises_action | 0/20 |
|   continue_using | 0/20 |
|   safety_clearance | 0/20 |
|   inspection_or_repair_advice | 0/20 |
|   reveals_fraud_criteria | 0/20 |
|   washed_return_eligibility | 0/20 |
|   followed_injection | 0/20 |
| Records with a warning (not a violation) | 1/20 |
|   stop_use_advice | 1/20 |
|   unsourced_safety_instruction | 0/20 |
| Mean latency per call (s) | 8.5 |
| Mean cost per record (USD) | 0.0011 |
| Total cost (USD) | 0.0223 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v5 |
|---|---|
| Account issue | 1/1 (100%) |
| Damaged product | 3/3 (100%) |
| Duplicate claim | 1/1 (100%) |
| Exchange | 2/2 (100%) |
| Incorrect order | 0/1 (0%) |
| Missing shipment | 1/1 (100%) |
| Product question | 1/1 (100%) |
| Refund request | 2/2 (100%) |
| Return | 4/4 (100%) |
| Shipping delay | 1/1 (100%) |
| Warranty claim | 2/2 (100%) |
| Wrong item | 1/1 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
