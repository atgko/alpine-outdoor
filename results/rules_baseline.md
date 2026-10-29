# Checkpoint 1: rules only router vs assigned_owner

Data split: all 48 (tune 28 + holdout 20) | Mode: structured fields plus keyword extraction from policy_relevant_facts (no customer message, no LLM) | Prompt version: none (rules only) | Model: none | Cases: 48

Run log: `runs/rules_baseline_20261029T024611Z.jsonl`. The label is `assigned_owner`, a current process step, not an approved final action. The sample is not representative. The rules were developed with knowledge of all 48 cases, so holdout numbers are not an unbiased estimate.

## Match rate

| Config | All 48 | Tune 28 | Holdout 20 |
|---|---|---|---|
| 9 client rules only | 39/48 (81.2%) | 22/28 (78.6%) | 17/20 (85.0%) |
| Client rules + W1 (without team proposed) | 43/48 (89.6%) | 24/28 (85.7%) | 19/20 (95.0%) |
| Client rules + W1 + T1 fulfillment error | 42/48 (87.5%) | 23/28 (82.1%) | 19/20 (95.0%) |
| Client rules + W1 + T2 stalled shipment | 45/48 (93.8%) | 26/28 (92.9%) | 19/20 (95.0%) |
| Client rules + W1 + T1 + T2 (with team proposed) | 44/48 (91.7%) | 25/28 (89.3%) | 19/20 (95.0%) |

## Mismatches without team proposed rules (client rules + W1)

Data split: all 48 | Mode: structured fields plus keyword extraction from policy_relevant_facts (no customer message, no LLM) | Prompt version: none (rules only) | Model: none | Cases: 48

| Case | Split | assigned_owner | Rules primary_route | Fired rules | Required approvals |
|---|---|---|---|---|---|
| CS-5214 | holdout | Fulfillment Support | Support Representative | none (default) | - |
| CS-5220 | tune | Fulfillment Support | Support Representative | none (default) | - |
| CS-5223 | tune | Fulfillment Support | Support Representative | none (default) | - |
| CS-5243 | tune | Shipping Support | Support Representative | none (default) | - |
| CS-5244 | tune | Support Representative | Support Lead | R4 | Support Lead |

## Mismatches with team proposed rules (client rules + W1 + T1 + T2)

Data split: all 48 | Mode: structured fields plus keyword extraction from policy_relevant_facts (no customer message, no LLM) | Prompt version: none (rules only) | Model: none | Cases: 48

| Case | Split | assigned_owner | Rules primary_route | Fired rules | Required approvals |
|---|---|---|---|---|---|
| CS-5204 | tune | Support Representative | Fulfillment Support | T1 | Fulfillment Support |
| CS-5225 | tune | Support Representative | Fulfillment Support | T1 | Fulfillment Support |
| CS-5237 | holdout | Support Representative | Fulfillment Support | T1 | Fulfillment Support |
| CS-5244 | tune | Support Representative | Support Lead | R4 | Support Lead |

## Rule status counts (with team proposed config)

Data split: all 48 | Mode: structured fields plus keyword extraction from policy_relevant_facts (no customer message, no LLM) | Prompt version: none (rules only) | Model: none | Cases: 48

| Rule | Origin | Fired | Not fired | Cannot evaluate |
|---|---|---|---|---|
| R1 | client | 8 | 40 | 0 |
| R2 | client | 5 | 41 | 2 |
| R3 | client | 0 | 48 | 0 |
| R4 | client | 5 | 41 | 2 |
| R5 | client | 2 | 45 | 1 |
| R6 | client | 5 | 43 | 0 |
| R7 | client | 6 | 42 | 0 |
| R8 | client | 3 | 0 | 45 |
| R9 | client | 2 | 46 | 0 |
| W1 | policy_derived | 5 | 43 | 0 |
| T1 | team_proposed | 5 | 43 | 0 |
| T2 | team_proposed | 2 | 43 | 3 |
