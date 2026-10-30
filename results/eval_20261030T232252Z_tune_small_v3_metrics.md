# Metrics: eval_20261030T232252Z_tune_small_v3

Run logs: C:/Users/athav/OneDrive/Documents/Alpine Outdoor/runs/eval_20261030T232252Z_tune_small_v3.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: tune | Mode: fields_only | Prompt versions: v3 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v3 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 18/28 (64%) |
| Route = policy-consistent label | 19/28 (68%) |
| Required approval recall | 11/14 (79%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 12/15 (80%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/28 |
| KB-710 cited without caveat (v3 onwards) | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 0/28 |
|   promises_action | 0/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 1/28 |
|   stop_use_advice | 1/28 |
|   unsourced_safety_instruction | 0/28 |
| Mean latency per call (s) | 8.8 |
| Mean cost per record (USD) | 0.0011 |
| Total cost (USD) | 0.0313 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v3 |
|---|---|
| Account issue | 0/1 (0%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 2/4 (50%) |
| Potential fraud | 1/1 (100%) |
| Product question | 2/4 (50%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 2/5 (40%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: tune | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v3 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 28

| Metric | v3 |
|---|---|
| API ok | 28/28 (100%) |
| Schema valid (v2 onwards) | 28/28 (100%) |
| Route = assigned_owner | 21/28 (75%) |
| Route = policy-consistent label | 22/28 (79%) |
| Required approval recall | 11/14 (79%) |
| No order number flagged | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | 13/15 (87%) |
| Extraction: order_number_present | 15/15 (100%) |
| Extraction: product_category | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | 0/28 |
| KB-710 cited without caveat (v3 onwards) | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a |
| Records with a guardrail violation | 0/28 |
|   promises_action | 0/28 |
|   continue_using | 0/28 |
|   safety_clearance | 0/28 |
|   inspection_or_repair_advice | 0/28 |
|   reveals_fraud_criteria | 0/28 |
|   washed_return_eligibility | 0/28 |
|   followed_injection | 0/28 |
| Records with a warning (not a violation) | 1/28 |
|   stop_use_advice | 1/28 |
|   unsourced_safety_instruction | 0/28 |
| Mean latency per call (s) | 9.0 |
| Mean cost per record (USD) | 0.0012 |
| Total cost (USD) | 0.0325 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v3 |
|---|---|
| Account issue | 0/1 (0%) |
| Chargeback | 1/1 (100%) |
| Damaged product | 1/1 (100%) |
| Exchange | 1/1 (100%) |
| Incorrect order | 1/2 (50%) |
| Missing shipment | 2/4 (50%) |
| Potential fraud | 1/1 (100%) |
| Product question | 3/4 (75%) |
| Product safety concern | 2/2 (100%) |
| Refund request | 2/2 (100%) |
| Return | 4/5 (80%) |
| Shipping delay | 0/1 (0%) |
| Warranty claim | 3/3 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
