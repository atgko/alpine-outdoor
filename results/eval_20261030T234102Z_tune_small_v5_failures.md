# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 8 records with any failure.

## CS-5213 | fields_only | v5 | severity 20

route=Support Lead owner=Support Lead policy=Support Lead | approvals=Support Lead (expected Support Lead) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5213",
  "issue_type": "return",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date, needed to confirm the 30-calendar-day window under POL-RETURN and KB-101",
    "Purchase channel (online or retail store), needed to determine the applicable return workflow",
    "Item condition assessment from the attached photos, since the item is reported as worn with visible dirt",
    "Prior related claims in the last 90 days, which the rule layer could not evaluate (R8)"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order date is 2026-09-25 and the order is marked delivered.",
    "Purchase amount is $210 USD.",
    "Customer reports the item is worn and shows visible dirt.",
    "Customer has changed the return reason twice.",
    "Customer provided photos.",
    "Rule R4 fired: the return may be outside the 30-day window, or the item may be used or its condition unclear. No automatic approval applies, and policy review is required.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": [
    "R4"
  ],
  "recommended_route": "Support Lead",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "POL-RETURN",
    "KB-101"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "Rule R4 fired, so the case needs a Support Lead policy review. The item is reported as worn with visible dirt, so its condition is unclear and the photos need assessment against the resalable and unused requirements in POL-RETURN. The delivery date and purchase channel are not in the case, so the return window and workflow cannot be confirmed. Rule R8 could not be evaluated. The approved sources do not cover how to handle a return denied for use, so this needs human judgment. No refund, return label, or other outcome can be confirmed or promised at this stage.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about your return request for your recent order. We have received your refund request and the photos you attached.\n\nYour request will be reviewed by a member of our support team, who will check the order details, the return eligibility under our Return, Exchange, and Refund Policy, and the condition of the item shown in your photos. We are not able to confirm a refund or a return label at this time, and this review may take some time.\n\nTo help us complete the review, please reply with:\n- The delivery date shown on your order, or the date you received the item\n- Where you purchased the item (online or a retail store)\n- Any additional details about the condition of the item\n\nIf you have your order number handy, please include it in your reply so we can locate your order.\n\nWe appreciate your patience.\n\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5213: Customer requests refund for outdoor clothing, $210, order date 2026-09-25, marked delivered. Customer reports item is worn with visible dirt and has changed return reason twice; photos attached. Rule R4 fired (possible outside 30-day window, used item, or unclear condition), routed to Support Lead for policy review. R8 not evaluated (prior_related_claims_90d unknown). Missing: delivery date, purchase channel, condition assessment from photos. No refund or return label confirmed or promised. Draft reply sent requesting delivery date, purchase channel, and item condition details. Sources: POL-RETURN, KB-101."
}
```

## CS-5248 | fields_plus_simulated_message | v5 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=Fraud and Payment Operations (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{"case_id":"CS-5248","issue_type":"fraud_signal","product_category":"Outdoor clothing","order_number_present":true,"missing_information":["Proof of purchase or other supporting evidence (none provided)","Reason for the refund request (not stated in customer message)","Confirmation of the delivery address on file for the order and any address change history, to be checked by a representative through the current authorized workflow"],"customer_requested_outcome":"Refund to the original payment card for jacket on order AO-418248; customer also asks that future correspondence use their newest address.","key_facts":["Order AO-418248 provided; order date 2026-10-05; delivery status Delivered; purchase amount 480 USD.","Customer requests a refund and asks that it be sent to their card.","Customer states they have moved again and asks that the newest address be used for anything sent.","Case is routed by the deterministic rule layer to Fraud and Payment Operations; no evidence was provided with the case.","The case includes an address change request, which is not covered by a current authoritative source (KB-710 is outdated)."],"rule_flags":["R8"],"recommended_route":"Fraud and Payment Operations","required_approvals":["Fraud and Payment Operations"],"sources_cited":["POL-RETURN","NOTE-KNOWLEDGE-QUALITY","KB-710"],"confidence":"low","needs_human_judgment_reason":"Rule R8 fired and the case must go to Fraud and Payment Operations before any refund or address decision. The item condition, return eligibility, and whether the order falls within the 30-day window are not established by the case facts (delivery is recorded, but the return date and usage condition are not). Under POL-RETURN, a refund cannot be issued until the authorized return or refund workflow confirms eligibility and required approval. The address change request cannot be actioned from KB-710, which is outdated; a representative must verify the current workflow. Detailed fraud criteria are not available to front line representatives and are not discussed here.","draft_reply":"Hello,\n\nThank you for contacting Alpine Outdoor about order AO-418248. We have received your refund request for the jacket and your note about your updated address.\n\nYour request has been referred to a team that reviews refund requests. They will review the request and the order details before any decision is made, and we are not able to confirm a refund or its timing at this stage. A representative will also verify our current process for address updates before any change is made to your account or to future shipments.\n\nTo help with the review, please reply with the reason for your return and any details you can share about the jacket's condition and when it was delivered. If you have proof of purchase or other supporting information, please include it.\n\nBest regards,\nAlpine Outdoor Customer Support","draft_case_note":"CS-5248: Customer requests refund for jacket on order AO-418248 (delivered, 480 USD, ordered 2026-10-05) and asks that newest address be used. Rule R8 fired; routed to Fraud and Payment Operations for review. No evidence provided. Return eligibility, item condition, and reason for return not established. No refund or address change has been made or promised. Address change must be verified against the current workflow (KB-710 outdated). Draft reply requests return reason and supporting details. Representative to review before sending."}
```

## CS-5204 | fields_only | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date, needed to confirm the 30-day return window under POL-RETURN",
    "Whether the order was placed online or at a retail store, since the return and exchange workflows differ",
    "Prior related claims in the last 90 days, required to evaluate rule R8 (currently cannot be evaluated)",
    "Confirmation of the color ordered versus the color received, beyond the attached photo"
  ],
  "customer_requested_outcome": "Exchange",
  "key_facts": [
    "Customer reports receiving a jacket in the wrong color.",
    "Customer states the item is unused.",
    "Order number was provided; order date is 2026-10-04.",
    "Order status is Delivered.",
    "Purchase amount is $174.",
    "Customer submitted a photo as evidence.",
    "Contact channel is phone.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN", "NOTE-KNOWLEDGE-QUALITY"],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Fulfillment Support for a possible fulfillment error (T1). Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the representative should check claim history before proceeding. The delivery date and purchase channel are missing, so the 30-day return window and the applicable workflow cannot be confirmed. Whether the item is unused and in resalable condition, and whether the color error is confirmed, also need representative review. POL-RETURN says exchanges for eligible unused items are subject to inventory and that fulfillment errors go through the authorized replacement or exchange workflow after order verification. No approval has been made.",
  "draft_reply": "Thank you for calling Alpine Outdoor and for sending the photo of the jacket. I'm sorry the color you received isn't the one you ordered. I've noted your request for an exchange and sent your case to our Fulfillment Support team to review the order. They will check the order details and the photo against what was shipped. Before that review, could you please confirm the date your order was delivered and whether you bought it online or at one of our retail stores? Please also confirm that the jacket has not been worn, washed, or had its tags removed. Once the review is complete, a representative will contact you with the next steps. Exchanges depend on eligibility and inventory availability, so I can't confirm the outcome today.",
  "draft_case_note": "CS-5204: Customer reports receiving a jacket in the wrong color (outdoor clothing, $174, delivered, order date 2026-10-04). Customer states the item is unused and provided a photo. Customer requests an exchange. Rule T1 fired (possible fulfillment error), routed to Fulfillment Support. Rule R8 could not be evaluated (prior_related_claims_90d unknown). Missing: delivery date, purchase channel (online vs. store), prior claims count, confirmation of ordered vs. received color. Return window and eligibility not confirmed. No exchange, refund, or approval has been made or promised. Draft reply asks customer for delivery date, purchase channel, and condition confirmation; case sent to Fulfillment Support for review. Confidence low. Sources: POL-RETURN, NOTE-KNOWLEDGE-QUALITY."
}
```

## CS-5204 | fields_plus_simulated_message | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "prior_related_claims_90d (required for rule R8, which could not be evaluated)",
    "Fulfillment Support confirmation of the fulfillment error and the item that was shipped"
  ],
  "customer_requested_outcome": "Exchange the orange rain jacket for the blue rain jacket from order AO-418204",
  "key_facts": [
    "Customer ordered a blue rain jacket on order AO-418204 and received an orange jacket.",
    "Customer reports the item is unused.",
    "Order date is 2026-10-04 and delivery status is Delivered.",
    "Purchase amount is $174. Channel is Phone.",
    "Customer provided a photo.",
    "Rule T1 fired (possible fulfillment error) and routes the case to Fulfillment Support.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN"],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Fulfillment Support for a possible fulfillment error, and that routing is mandatory. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the representative should check that fact before proceeding. The policy allows exchanges for a different color only for eligible unused items and subject to inventory availability, and fulfillment errors go through the authorized replacement or exchange workflow after order verification. The sources do not confirm blue jacket inventory or the outcome of order verification. The representative must confirm the item's condition and eligibility in the authorized workflow. Nothing in this draft approves or commits to an exchange.",
  "draft_reply": "Thank you for contacting Alpine Outdoor and for sending the photo. We have noted that you received an orange rain jacket on order AO-418204 instead of the blue one you ordered. Your case has been referred to our Fulfillment Support team, who will verify the order and review your request for an exchange under our standard exchange process. Exchanges for a different color are subject to eligibility and inventory availability, so we cannot confirm the exchange yet. A representative will contact you with the outcome of that review.",
  "draft_case_note": "Customer (phone) reports receiving orange rain jacket instead of blue on order AO-418204 (ordered 2026-10-04, delivered, $174). States item is unused; photo attached. Requests exchange to blue. Rule T1 fired and routes to Fulfillment Support (required approval: Fulfillment Support). Rule R8 not evaluated: prior_related_claims_90d unknown. Per POL-RETURN, a fulfillment error may be corrected via the authorized replacement/exchange workflow after order verification, and color exchanges are subject to eligibility and inventory. No exchange approved or promised in this draft. Draft reply sent for representative review. Representative to confirm order verification, item condition, inventory, and R8 data before any action."
}
```

## CS-5225 | fields_only | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5225",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date (case shows delivery status only; delivery date needed to check the 30-day window under POL-RETURN)",
    "Confirmation that the item is unused, in resalable condition, and includes original tags or packaging where applicable",
    "Purchase channel confirmation (standard online purchase or retail store purchase), since the return path differs"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Customer ordered a duplicate item by mistake",
    "Customer states the duplicate item is unopened",
    "Order date is 2026-10-06",
    "Delivery status is Delivered",
    "Purchase amount is $47 USD",
    "No evidence was provided",
    "Order number was provided"
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN", "KB-101"],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer fired T1 (possible fulfillment error) and routes to Fulfillment Support. The customer describes an over-order by mistake, which may be a customer ordering error rather than a fulfillment error. The rule layer result is treated as mandatory, so the case stays with Fulfillment Support, but the representative should confirm the fact pattern. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the rule layer result is incomplete. Item condition is unverified: the customer says unopened, but tags, packaging, and resalability are not confirmed. The delivery date is missing, so the 30-day window under POL-RETURN cannot be checked. KB-101 says not to issue a return label for items requiring review until that review is complete. No approved source covers refunds for over-orders outside the standard policy, so the representative must decide how the policy applies.",
  "draft_reply": "Thank you for reaching out about your order. I understand you ordered a duplicate item by mistake and that it has not been opened. I have passed your request to our Fulfillment Support team to review your order and check whether a return is eligible. No return label or refund has been approved yet, and I can't confirm an outcome until that review is complete. To help with the review, please reply with the date your order was delivered, and confirm whether the item is unused and still has its original tags or packaging. Please also let us know whether the order was placed online or at one of our stores.",
  "draft_case_note": "Customer requests refund for duplicate outdoor clothing item ordered by mistake; customer reports item unopened. Order number provided; order date 2026-10-06; delivery status Delivered; amount $47 USD. No evidence provided. Rule T1 fired (possible fulfillment error); routed to Fulfillment Support, which is the required approval. R8 not evaluable (prior_related_claims_90d unknown). Missing: delivery date, item condition and tags/packaging confirmation, purchase channel. No refund or return label issued or promised. Customer told the request is under review and asked for missing details. Confidence low due to conflicting fact pattern (over-order vs. fulfillment error), unverified condition, and missing delivery date."
}
```

## CS-5225 | fields_plus_simulated_message | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5225",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Verification that the unopened duplicate item is unused, resalable, and has original tags or packaging, as required by policy. The customer's statement is not verified.",
    "Delivery date, needed to confirm the 30-day return window, which runs from delivery. Only the order date (2026-10-06) and delivered status are in the case.",
    "Prior related claims in the last 90 days, needed for rule R8. This value is unknown, so R8 could not be evaluated."
  ],
  "customer_requested_outcome": "Refund for an unopened duplicate item ordered by mistake (order AO-418225)",
  "key_facts": [
    "Order AO-418225 was provided and the order date is 2026-10-06.",
    "Delivery status is Delivered. The customer reports ordering the same item twice by accident.",
    "The customer reports one duplicate is still unopened. No evidence was provided.",
    "Purchase amount is $47 USD.",
    "Rule T1 fired (possible fulfillment error) and routes the case to Fulfillment Support. Fulfillment Support approval is required.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": [
    "T1"
  ],
  "recommended_route": "Fulfillment Support",
  "required_approvals": [
    "Fulfillment Support"
  ],
  "sources_cited": [
    "POL-RETURN",
    "KB-101"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The return and refund eligibility depends on item condition, which is unverified. The customer says the duplicate is unopened, but policy requires the item to be unused, resalable, and to have original tags or packaging where applicable. The delivery date is also needed to confirm the 30-day window. The rule layer routed the case to Fulfillment Support for a possible fulfillment error, and this review is required before any return label or refund. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the representative should check that value in the authorized system. Nothing in the approved sources covers how a duplicate order should be handled beyond the standard return and fulfillment error workflows.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about order AO-418225. I'm sorry for the trouble with the duplicate order. I have received your request for a refund on the unopened duplicate item. Your request is being reviewed by our Fulfillment Support team, who will confirm whether the item meets our return requirements. To help with that review, please confirm that the unopened item is in its original condition, with tags or packaging still attached where applicable. Our standard return window is 30 calendar days from delivery, and the team will check the delivery date on your order. I cannot confirm a refund or return label until that review is complete.",
  "draft_case_note": "CS-5225: Customer reports accidental duplicate order (AO-418225, order date 2026-10-06, delivered, $47). Customer states one duplicate is unopened. No evidence provided. Rule T1 fired and routed to Fulfillment Support (approval required). R8 not evaluated: prior_related_claims_90d unknown. Missing: item condition verification (unused, resalable, tags/packaging), delivery date for 30-day window check. Draft reply sent requesting condition confirmation; no refund or return label promised or issued. Sources: POL-RETURN, KB-101. Confidence low. Route: Fulfillment Support."
}
```

## CS-5244 | fields_only | v5 | severity 5

route=Support Lead owner=Support Representative policy=Support Lead | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5244",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date (only delivery status is provided; needed to confirm the 30-day window)",
    "Purchase channel: online or retail store (determines which return workflow applies)",
    "Current condition of the item beyond the reported wash and tag removal",
    "Customer's reason for the return",
    "Any supporting evidence (none provided)"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order number provided; order date 2026-09-27; delivery status: Delivered",
    "Purchase amount: $55 USD",
    "Customer reports the item was washed once and tags were removed",
    "No evidence provided",
    "Rule R4 fired: return timing or item condition is unclear, so no automatic approval and policy review is required",
    "One control check could not be evaluated because case data is incomplete; the representative should review the case with that gap in mind"
  ],
  "rule_flags": ["R4"],
  "recommended_route": "Support Lead",
  "required_approvals": ["Support Lead"],
  "sources_cited": ["POL-RETURN", "KB-101", "KB-510"],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Support Lead (R4) because return timing and item condition are unclear. The item was washed and had its tags removed, and the policy requires unused, resalable condition with original tags where applicable. The approved sources do not establish whether washing or tag removal affects eligibility, and KB-510 states that return eligibility depends on policy and product condition, so a representative cannot confirm eligibility from the sources. The delivery date and purchase channel are also missing, so the 30-day window cannot be checked. No refund can be issued until the authorized review is complete. One control check could not be evaluated due to missing case data, which the reviewer should account for.",
  "draft_reply": "Thank you for reaching out about your return request for order details on file. I'm sorry for any inconvenience. Your request for a refund has been referred to a Support Lead, who will review your order against our return policy. This review is not complete, so I can't confirm whether a refund will be approved at this time. To help with the review, could you please share the date your order was delivered and whether you purchased it online or in a store? Please also tell us the reason for your return. If you have any photos or other details about the item's condition, please include those as well. We'll follow up once the review is complete.",
  "draft_case_note": "CS-5244: Customer requests refund for outdoor clothing (order number provided, $55, order date 2026-09-27, delivered). Customer reports item was washed once and tags removed. No evidence provided. Rule R4 fired (timing or condition unclear); routed to Support Lead for policy review. Delivery date, purchase channel, return reason, and item condition are missing. No refund or return label has been issued or promised. Eligibility not confirmed. Sources: POL-RETURN, KB-101, KB-510."
}
```

## CS-5244 | fields_plus_simulated_message | v5 | severity 5

route=Support Lead owner=Support Representative policy=Support Lead | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5244",
  "issue_type": "return",
  "product_category": "Outdoor clothing (waterproof jacket)",
  "order_number_present": true,
  "missing_information": [
    "Delivery date, needed to confirm the 30-day return window under POL-RETURN",
    "Description of the item's current condition beyond 'washed once and tags removed'",
    "Whether the item is unused and resalable apart from washing and tag removal",
    "Value of prior_related_claims_90d, needed before rule R8 can be evaluated"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Customer provided order AO-418244 for a waterproof jacket, order date 2026-09-27, status Delivered, purchase amount $55 USD",
    "Customer washed the item once and removed the tags",
    "Customer says the item does not fit as hoped and asks whether a refund is possible",
    "No evidence was provided",
    "Rule R4 fired: return is outside 30 days, or the item is used or its condition is unclear. This requires policy review and routes to Support Lead",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown",
    "POL-RETURN requires that products be unused and in resalable condition for standard returns. Refunds may not be issued until the authorized workflow confirms eligibility and required approval",
    "KB-510 states that washing or tag removal must not be described as keeping return eligibility. Return eligibility depends on policy and product condition"
  ],
  "rule_flags": ["R4"],
  "recommended_route": "Support Lead",
  "required_approvals": ["Support Lead"],
  "sources_cited": ["POL-RETURN", "KB-101", "KB-510", "NOTE-KNOWLEDGE-QUALITY"],
  "confidence": "low",
  "needs_human_judgment_reason": "The item was used (washed once) and tags were removed, and the delivery date needed to confirm the 30-day window is not provided. Rule R4 requires Support Lead policy review, and rule R8 cannot be evaluated because prior_related_claims_90d is unknown. The approved sources do not state whether washing and tag removal is an exception to the return policy, so eligibility cannot be determined from the sources. The customer's fit concern is not addressed by the sources as a return reason for a used item. Support Lead should decide eligibility and whether any exception applies.",
  "draft_reply": "Thank you for your message about order AO-418244. I'm sorry the jacket doesn't fit the way you hoped. We have your order number. Because the jacket has been washed and the tags have been removed, your return needs to be reviewed under our return policy before any decision can be made. I can't confirm that the jacket is eligible for a refund at this time, and I can't promise a refund. I'm sending your request to our Support Lead for that review. Please also note that we need the delivery date for your order to confirm the return window. If you can share it, that would help the review. A team member will contact you with the outcome.",
  "draft_case_note": "CS-5244: Customer requests refund for waterproof jacket, order AO-418244 (order date 2026-09-27, Delivered, $55). Customer washed item once and removed tags; reports fit issue. No evidence provided. Rule R4 fired (used or condition unclear; outside 30 days possible), routed to Support Lead. R8 not evaluable: prior_related_claims_90d unknown. Delivery date needed to confirm return window. No refund or return label issued and none promised. Draft reply sent for representative review; customer told the request is under review and to provide delivery date."
}
```

