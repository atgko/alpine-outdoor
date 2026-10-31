# Open Questions and Team Decisions

Ambiguities found in the client policy or data. Each one records what the code does now and whether it is a team decision or still open. None of the team decisions are client rules.

## Q1. Route priority when several rules fire
The client does not say which route wins when several rules fire (for example a $740 warranty claim).
**Team decision (made after seeing the sample cases):** Fraud and Payment Operations, Product Safety, Warranty Team, Support Lead, Shipping or Fulfillment Support, Support Representative. Support Lead stays in `required_approvals` when the amount is over $500. **Client should confirm.**

## Q2. Owner for rule 4 (outside 30 days or condition unclear)
Rule 4 says "route for policy review or exception handling" but names no team. In the sample, CS-5207 (62 days) went to Support Lead, but CS-5244 (washed once, tags removed) went to Support Representative.
**Team decision:** route outside window and used item returns to Support Lead. CS-5244 is a known miss against `assigned_owner`. **Open:** is a washed jacket "condition unclear" under rule 4, or a standard representative review?

## Q3. Owner for rule 5 (delivered but missing)
Rule 5 says "open a delivery investigation" but names no team.
**Team decision:** Shipping Support, matching CS-5203 and CS-5230.

## Q4. Value used for rule 7 (over $500)
Rule 7 is about the refund or replacement value. The CSV only has `purchase_amount_usd` (order or item value).
**Current behavior:** purchase amount is used as the refund value. **Open:** for CS-5242 (four jackets, $1,200) the actual refund could be partial.

## Q5. Definition of "repeated claims" in rule 8
The client does not define "repeated". The field it needs, `prior_related_claims_90d`, is not in the CSV.
**Current behavior:** the threshold is 2 or more related claims in 90 days (placeholder, never used because the field is missing). Rule 8 fires from issue type (chargeback, duplicate claim, potential fraud) or text signals. When none of those are present, rule 8 reports "cannot evaluate" because the claim count is unknown. **Client should define the threshold.**

## Q6. CS-5213: return reason changed twice
Is a changed return reason "inconsistent order details" under rule 8? The sample routes CS-5213 to Support Lead ("possible policy abuse"), not Fraud.
**Team decision:** do not treat it as a fraud signal. **Open for the client.**

## Q7. No client rule routes to the Warranty Team
None of the nine section 4 rules names the Warranty Team, but the sample assigns four cases to it.
**Resolved (team confirmed, 2026-10-28):** keep rule W1 (warranty claim goes to the Warranty Team) as a policy derived rule, sourced from policy section 2 and KB 318 ("Warranty staff determine whether the concern is covered"). It is labeled `policy_derived` and kept separate from the nine client rules in code, README and results. Checkpoint 1 reports results with and without it (39/48 client rules only, 43/48 with W1). The client has still not stated a warranty routing rule, so this remains a team interpretation of policy text.

## Q8. Stalled shipment owner (TEAM PROPOSED rule T2)
The proposed rule says "Shipping Support or Fulfillment Support".
**Team decision:** not yet shipped (label created or processing) goes to Fulfillment Support, in transit goes to Shipping Support.

## Q9. When does a fulfillment error go to Fulfillment Support? (TEAM PROPOSED rule T1)
In the sample, CS-5214 (wrong tent) and CS-5223 (two left boots) went to Fulfillment Support, but CS-5204 (wrong jacket color) and CS-5237 (different model) went to Support Representative. The keyword "duplicate" also matches CS-5225, where the customer ordered twice by mistake (not a fulfillment error).
**Team decision:** keep T1 as written, do not tune it to the data, and report results with and without it. **Open for the client:** what decides whether a pick error is handled by a representative or by Fulfillment Support?
**Update 2026-10-30 (after Checkpoint 3):** T1 lowers accuracy. Rules only (Checkpoint 1, all 48 cases) it is net minus 1 case. In Checkpoint 3 (tune set, 28 cases, claude-haiku-5-5) the only v4 and v5 route misses against the policy label are CS-5204 and CS-5225, both caused by T1, in both modes. **Decision:** leave T1 unchanged for the midterm. **Planned change for the final submission:** disable T1 or refine it (for example, exclude "duplicate" orders placed by the customer, as in CS-5225), then rerun the tune set before any holdout run.
**Update 2026-10-31 (after the final evaluation):** T1 was left unchanged for the midterm and the holdout ran with T1 as written (`runs/eval_20261031T165427Z_holdout_small_v5.jsonl`, 20 cases, both modes, v5, claude-haiku-5-5). The planned change above was not made before that run. On the holdout T1 fired on two cases: CS-5214 matches `assigned_owner` and CS-5237 does not, in both modes. The holdout is used up, so any later T1 change can only be measured on the tune set.

## Q10. Store returns cannot be identified
`purchase_channel` is not in the CSV, so rule 3 (store return) can never be evaluated from the data.
**Current behavior:** purchase channel is inferred as online when a delivery status exists, otherwise unknown. Rule 3 reports "not fired" for shipped orders and "cannot evaluate" otherwise.

## Q11. Do the return rules apply to exchanges?
The return policy covers returns and exchanges of unused items together.
**Current behavior:** rules 2 and 4 apply to issue types `return` and `exchange`, not to `refund`.

## Q12. 30 day window start date
Online returns count 30 days from delivery and store returns from purchase. The CSV has no delivery date or case received date.
**Current behavior:** the window is read from the `policy_relevant_facts` text ("within 30 days", "62 days after delivery", "outside window") and labeled `extracted`. Otherwise unknown.

## Q13. Shipping Support and Fulfillment Support at the same priority level
If both fire on one case, Shipping Support is listed first only so the result is deterministic. No sample case triggers both.

## Q14. Policy-consistent route labels (2026-10-30)
`assigned_owner` is a process label. The user asked for route accuracy to be reported twice: against `assigned_owner`, and as a policy-consistent view.
**Decision applied:** the policy-consistent label equals `assigned_owner` unless a client rule (section 4) requires a different route and the reading is a recorded team decision. TEAM PROPOSED rules (T1, T2) never create an override. Checked against the Checkpoint 1 rules baseline on all 48 cases: the only case that qualifies is CS-5244 (washed jacket, tags removed), relabeled Support Lead under client rule 4 and team decision Q2. The warranty cases where client rules alone disagree (CS-5206, 5216, 5226, 5246) already match `assigned_owner` once W1 applies, so they need no override. Stored in `eval/policy_labels.json`. **Open for the client:** confirm that rule 4 reviews belong to Support Lead.
