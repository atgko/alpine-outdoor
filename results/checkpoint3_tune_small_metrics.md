# Metrics: checkpoint3_tune_small

Run logs: runs/eval_20261030T230955Z_tune_small_v1.jsonl, runs/eval_20261030T231525Z_tune_small_v2.jsonl, runs/eval_20261030T232252Z_tune_small_v3.jsonl, runs/eval_20261030T233215Z_tune_small_v4.jsonl, runs/eval_20261030T234102Z_tune_small_v5.jsonl. Every number comes from these logs. Guardrails recomputed with the current src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a selected sample, not representative.

## claude-haiku-5-5 | fields_only

Data split: tune | Mode: fields_only | Prompt versions: v1, v2, v3, v4, v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 140

| Metric | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| API ok | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) |
| Schema valid (v2 onwards) | n/a | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) |
| Route = assigned_owner | 23/28 (82%) | 20/28 (71%) | 18/28 (64%) | 25/28 (89%) | 25/28 (89%) |
| Route = policy-consistent label | 22/28 (79%) | 21/28 (75%) | 19/28 (68%) | 26/28 (93%) | 26/28 (93%) |
| Required approval recall | n/a | 8/14 (57%) | 11/14 (79%) | 14/14 (100%) | 14/14 (100%) |
| No order number flagged | n/a | 7/7 (100%) | 7/7 (100%) | 7/7 (100%) | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | n/a | 15/15 (100%) | 12/15 (80%) | 13/15 (87%) | 12/15 (80%) |
| Extraction: order_number_present | n/a | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Extraction: product_category | n/a | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | n/a | n/a | 0/28 | 0/28 | 0/28 |
| KB-710 cited without caveat (v3 onwards) | n/a | n/a | 0/28 | 0/28 | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a | n/a | n/a | 0/28 | 0/28 |
| Records with a guardrail violation | 6/28 | 5/28 | 0/28 | 1/28 | 1/28 |
|   promises_action | 6/28 | 4/28 | 0/28 | 1/28 | 1/28 |
|   continue_using | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   safety_clearance | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   inspection_or_repair_advice | 0/28 | 1/28 | 0/28 | 0/28 | 0/28 |
|   reveals_fraud_criteria | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   washed_return_eligibility | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   followed_injection | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
| Records with a warning (not a violation) | 5/28 | 6/28 | 1/28 | 0/28 | 0/28 |
|   stop_use_advice | 5/28 | 6/28 | 1/28 | 0/28 | 0/28 |
|   unsourced_safety_instruction | 1/28 | 2/28 | 0/28 | 0/28 | 0/28 |
| Mean latency per call (s) | 4.8 | 6.7 | 8.8 | 8.2 | 8.5 |
| Mean cost per record (USD) | 0.0004 | 0.0007 | 0.0011 | 0.0010 | 0.0011 |
| Total cost (USD) | 0.0121 | 0.0201 | 0.0313 | 0.0294 | 0.0303 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_only):

| Issue type | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| Account issue | 1/1 (100%) | 1/1 (100%) | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) |
| Chargeback | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Damaged product | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Exchange | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Incorrect order | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) |
| Missing shipment | 4/4 (100%) | 2/4 (50%) | 2/4 (50%) | 4/4 (100%) | 4/4 (100%) |
| Potential fraud | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Product question | 3/4 (75%) | 2/4 (50%) | 2/4 (50%) | 4/4 (100%) | 4/4 (100%) |
| Product safety concern | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) |
| Refund request | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 1/2 (50%) | 1/2 (50%) |
| Return | 4/5 (80%) | 3/5 (60%) | 2/5 (40%) | 4/5 (80%) | 4/5 (80%) |
| Shipping delay | 0/1 (0%) | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) |
| Warranty claim | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |

## claude-haiku-5-5 | fields_plus_simulated_message

Data split: tune | Mode: fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v1, v2, v3, v4, v5 | Model: claude-haiku-5-5 (anthropic) | Cases: 28 | Records: 140

| Metric | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| API ok | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) |
| Schema valid (v2 onwards) | n/a | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) | 28/28 (100%) |
| Route = assigned_owner | 23/28 (82%) | 18/28 (64%) | 21/28 (75%) | 25/28 (89%) | 25/28 (89%) |
| Route = policy-consistent label | 22/28 (79%) | 19/28 (68%) | 22/28 (79%) | 26/28 (93%) | 26/28 (93%) |
| Required approval recall | n/a | 10/14 (71%) | 11/14 (79%) | 14/14 (100%) | 14/14 (100%) |
| No order number flagged | n/a | 7/7 (100%) | 7/7 (100%) | 7/7 (100%) | 7/7 (100%) |
| Extraction: issue_type (15 case subset) | n/a | 14/15 (93%) | 13/15 (87%) | 12/15 (80%) | 15/15 (100%) |
| Extraction: order_number_present | n/a | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Extraction: product_category | n/a | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) | 15/15 (100%) |
| Cited ids unknown (v3 onwards) | n/a | n/a | 0/28 | 0/28 | 0/28 |
| KB-710 cited without caveat (v3 onwards) | n/a | n/a | 0/28 | 0/28 | 0/28 |
| Safety cases routed to Product Safety | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |
| Model disagreed with rules (v4, v5) | n/a | n/a | n/a | 0/28 | 0/28 |
| Records with a guardrail violation | 4/28 | 4/28 | 0/28 | 1/28 | 1/28 |
|   promises_action | 4/28 | 3/28 | 0/28 | 1/28 | 1/28 |
|   continue_using | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   safety_clearance | 0/28 | 1/28 | 0/28 | 0/28 | 0/28 |
|   inspection_or_repair_advice | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   reveals_fraud_criteria | 0/28 | 1/28 | 0/28 | 0/28 | 0/28 |
|   washed_return_eligibility | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
|   followed_injection | 0/28 | 0/28 | 0/28 | 0/28 | 0/28 |
| Records with a warning (not a violation) | 6/28 | 3/28 | 1/28 | 0/28 | 0/28 |
|   stop_use_advice | 4/28 | 3/28 | 1/28 | 0/28 | 0/28 |
|   unsourced_safety_instruction | 4/28 | 1/28 | 0/28 | 0/28 | 0/28 |
| Mean latency per call (s) | 4.6 | 6.9 | 9.0 | 8.3 | 8.6 |
| Mean cost per record (USD) | 0.0004 | 0.0008 | 0.0012 | 0.0011 | 0.0011 |
| Total cost (USD) | 0.0118 | 0.0214 | 0.0325 | 0.0304 | 0.0314 |

Route = assigned_owner by CSV issue type (claude-haiku-5-5, fields_plus_simulated_message):

| Issue type | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| Account issue | 0/1 (0%) | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) |
| Chargeback | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Damaged product | 1/1 (100%) | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Exchange | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Incorrect order | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) | 1/2 (50%) |
| Missing shipment | 2/4 (50%) | 2/4 (50%) | 2/4 (50%) | 4/4 (100%) | 4/4 (100%) |
| Potential fraud | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) | 1/1 (100%) |
| Product question | 4/4 (100%) | 1/4 (25%) | 3/4 (75%) | 4/4 (100%) | 4/4 (100%) |
| Product safety concern | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) |
| Refund request | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) | 1/2 (50%) | 1/2 (50%) |
| Return | 5/5 (100%) | 4/5 (80%) | 4/5 (80%) | 4/5 (80%) | 4/5 (80%) |
| Shipping delay | 0/1 (0%) | 0/1 (0%) | 0/1 (0%) | 1/1 (100%) | 1/1 (100%) |
| Warranty claim | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |

## Consistency

No repeated runs in these logs (use run_eval --repeats 3).
