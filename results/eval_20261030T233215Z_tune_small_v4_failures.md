# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 8 records with any failure.

## CS-5248 | fields_only | v4 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=Fraud and Payment Operations (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5248",
  "issue_type": "fraud_signal",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Reason for the refund request",
    "Current condition of the item, including whether it has been used or washed and whether tags or packaging are present",
    "Return details or proof of return, if the item has been sent back",
    "Evidence supporting the request (none provided)",
    "Current status of the delivery address change, which must be verified by a representative under the current workflow"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order number provided; order dated 2026-10-05; status Delivered; purchase amount $480 USD",
    "Customer requests a refund",
    "No evidence provided",
    "Policy-relevant facts note multiple high-value refund requests and changing delivery addresses on the account",
    "Rule R8 fired and routes the case to Fraud and Payment Operations; that team is also the required approval",
    "KB-710 is outdated and not authoritative, so the current address change workflow must be verified by a representative",
    "Refund eligibility cannot be confirmed from approved sources until the authorized workflow reviews the case"
  ],
  "rule_flags": [
    "R8"
  ],
  "recommended_route": "Fraud and Payment Operations",
  "required_approvals": [
    "Fraud and Payment Operations"
  ],
  "sources_cited": [
    "POL-RETURN",
    "NOTE-KNOWLEDGE-QUALITY"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Fraud and Payment Operations (R8), which is a mandatory result. The case also involves a high-value refund request ($480) with no supporting evidence, an unknown item condition, and an account with multiple refund requests and changing delivery addresses. The approved sources do not establish refund eligibility for this situation, and KB-710 cannot be relied on for the address change workflow, so a representative must verify the current process. No refund or address decision should be communicated to the customer until the required review is complete.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about your order. We have received your refund request for this order, and it is now being reviewed by a specialist team. We are not able to confirm a refund or its timing at this stage. To help us complete our review, please reply with the reason you are requesting a refund, the current condition of the item (including whether it has been worn, used, or washed, and whether the original tags or packaging are still attached), and any supporting information you would like us to consider. Our team will follow up once the review is complete.",
  "draft_case_note": "CS-5248: Refund request on order (delivered, $480, outdoor clothing). No evidence provided. Rule R8 fired (repeated claims and unusual account activity) and routes to Fraud and Payment Operations, which is also the required approval. Policy-relevant facts note multiple high-value refund requests and changing delivery addresses. KB-710 is outdated; the current address change workflow must be verified by a representative. Customer asked for reason, item condition, and supporting information. No refund or address change has been approved or promised. Draft reply sent for review only; representative to confirm before sending and to route the case."
}
```

## CS-5248 | fields_plus_simulated_message | v4 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=Fraud and Payment Operations (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5248",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Item condition and whether it is unused and in resalable condition with original tags or packaging, as required by POL-RETURN",
    "Confirmation that the order falls within the 30-calendar-day return window from delivery (order date 2026-10-05; delivery date not provided)",
    "Verified current delivery address through the authorized workflow (KB-710 is outdated and not authoritative for address changes)",
    "Any supporting evidence (none provided)"
  ],
  "customer_requested_outcome": "Refund to the customer's card for the jacket on order AO-418248, and use of the customer's newest address for future shipments",
  "key_facts": [
    "Order AO-418248 is provided; order date 2026-10-05; delivery status is Delivered; purchase amount is $480 USD",
    "Customer requests a refund for a jacket and states they have moved and want the newest address used for anything sent",
    "No evidence was provided with the case",
    "Case facts note multiple high value refund requests with changing delivery addresses",
    "Rule layer fired R8 and requires routing to Fraud and Payment Operations, with Fraud and Payment Operations approval required",
    "Refund eligibility and address change cannot be confirmed from approved sources in this case; a refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval (POL-RETURN)"
  ],
  "rule_flags": [
    "R8"
  ],
  "recommended_route": "Fraud and Payment Operations",
  "required_approvals": [
    "Fraud and Payment Operations"
  ],
  "sources_cited": [
    "POL-RETURN",
    "KB-710",
    "NOTE-KNOWLEDGE-QUALITY"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Fraud and Payment Operations, and the case facts involve multiple high value refund requests with changing delivery addresses. Item condition, delivery date, and return window eligibility are not covered by the case facts and must be verified before any refund decision. The address change request cannot be processed from KB-710, which is outdated; the current workflow must be verified by a representative. Customer requested outcomes must not be confirmed in this reply.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about order AO-418248. We have received your refund request for the jacket and your note about your address.\n\nYour request is being reviewed by a specialist team. We are not able to confirm a refund or its timing at this stage. Once the review is complete, a representative will contact you with next steps.\n\nFor your address, our team must verify the current address update process before any change can be made. Please do not assume a change has been made. A representative will confirm the address on file with you.\n\nIf you have any additional information about the jacket, such as its condition or the date it was delivered, please reply to this email so it can be included in the review.\n\nThank you for your patience.\n\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5248: Customer requests refund for jacket on order AO-418248 (order date 2026-10-05, Delivered, $480) and asks that newest address be used. No evidence provided. Rule R8 fired and routes to Fraud and Payment Operations; approval required from Fraud and Payment Operations. Refund eligibility not verified: item condition, delivery date, and return window need confirmation under POL-RETURN. Address change not processed; KB-710 is outdated and the current workflow must be verified by a representative. No refund or address change has been approved or promised. Draft reply sent for representative review only."
}
```

## CS-5204 | fields_only | v4 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Verification of the received item's color against the order record (not covered in approved sources; requires Fulfillment Support review)",
    "prior_related_claims_90d (needed to evaluate rule R8)"
  ],
  "customer_requested_outcome": "Exchange",
  "key_facts": [
    "Customer reports receiving a jacket in the wrong color.",
    "Customer reports the item is unused.",
    "Customer provided a photo.",
    "Order date is 2026-10-04 and delivery status is Delivered.",
    "Purchase amount is $174.",
    "Contact channel is phone.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN"],
  "confidence": "low",
  "needs_human_judgment_reason": "The customer reports a wrong-color item and states it is unused, but the item's condition has not been verified and the photo has not been reviewed against the order record. Fulfillment errors may be corrected through the authorized exchange workflow after order verification (POL-RETURN), so the representative must confirm the fulfillment error and the item's eligibility. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the representative should check the claim history before any outcome is decided. Rule T1 routes the case to Fulfillment Support, which is the required approval.",
  "draft_reply": "Thank you for calling Alpine Outdoor and for sharing the photo of the jacket you received. I'm sorry the color was not what you ordered. I've referred your case to our Fulfillment Support team, who will review the order and the photo to check whether the item was shipped in error. They will confirm the next steps for an exchange. I can't confirm the outcome at this time. Until you hear from us, please keep the jacket unused and in its original packaging if you still have it.",
  "draft_case_note": "CS-5204: Customer called reporting a wrong-color jacket on a delivered order (order date 2026-10-04, $174). Customer states the item is unused and provided a photo. Requested outcome: exchange. Rule T1 fired (possible fulfillment error), routed to Fulfillment Support for review. Rule R8 not evaluated because prior_related_claims_90d is unknown. Item condition not verified. No exchange approved or promised. Customer told the case was referred to Fulfillment Support and asked to keep the item unused in original packaging."
}
```

## CS-5204 | fields_plus_simulated_message | v4 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Verification that order AO-418204 matches the blue rain jacket order and the orange item received",
    "Confirmation of item condition beyond the customer's statement that it is unused and the attached photo",
    "prior_related_claims_90d (rule R8 could not be evaluated)"
  ],
  "customer_requested_outcome": "Exchange of the orange rain jacket for the blue rain jacket",
  "key_facts": [
    "Customer ordered a blue rain jacket under order AO-418204 and received an orange one.",
    "Order date is 2026-10-04 and the order shows as delivered.",
    "Purchase amount is $174 USD.",
    "Customer states the item has not been worn. A photo was attached.",
    "Channel is phone.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN", "NOTE-KNOWLEDGE-QUALITY"],
  "confidence": "medium",
  "needs_human_judgment_reason": "The rule layer routes this case to Fulfillment Support as a possible fulfillment error, and that routing is mandatory. Eligibility for an exchange depends on verifying the order contents, confirming the item is unused and in resalable condition, and checking inventory for the blue jacket. These checks rest on the customer's statement and a photo, so a representative must confirm them. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so that input must be completed before the case is finalized.",
  "draft_reply": "Thank you for contacting Alpine Outdoor, and I'm sorry the rain jacket you received was not the blue one you ordered. I have noted that you received the orange jacket under order AO-418204 and that you have not worn it. Because this looks like a fulfillment error, I am sending your request to our Fulfillment Support team to review. They will verify the order and the item, and they will check whether an exchange for the blue jacket can be offered based on inventory availability. I cannot confirm the outcome of that review on this call. A representative will follow up with you once it is complete.",
  "draft_case_note": "CS-5204 (phone). Customer ordered blue rain jacket under AO-418204 (delivered, ordered 2026-10-04, $174) and received orange. States unused; photo attached. Requests exchange to blue. Rule T1 fired (possible fulfillment error); routed to Fulfillment Support for review. Rule R8 not evaluated: prior_related_claims_90d unknown. Pending: order verification, item condition check, inventory check for blue jacket. No exchange approved or promised to customer; customer told the request is under review and a representative will follow up. Sources: POL-RETURN, NOTE-KNOWLEDGE-QUALITY."
}
```

## CS-5225 | fields_only | v4 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5225",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date, needed to check whether the 30-day return window applies",
    "prior_related_claims_90d, needed to evaluate rule R8",
    "Whether the customer has a photo or other evidence of the unopened item and its packaging (none provided)",
    "Whether the duplicate item was ordered by the customer or caused by an error on Alpine Outdoor's side (conflicting with the rule layer's possible fulfillment error flag)"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Customer reports a duplicate item was ordered by mistake and is unopened.",
    "Order date is 2026-10-06 and delivery status is Delivered.",
    "Purchase amount is $47.",
    "No evidence was provided with the request.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN", "KB-101"],
  "confidence": "low",
  "needs_human_judgment_reason": "Confidence is low for several reasons. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so the rule layer result is incomplete. The delivery date is not provided, so the 30-day return window cannot be confirmed under POL-RETURN. The customer says they ordered the duplicate by mistake, but the rule layer flagged a possible fulfillment error, which points to a different cause; a representative should confirm which applies. The item is reported as unopened, but no evidence was provided. Under POL-RETURN, a refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval. No return label should be issued until the Fulfillment Support review is complete (KB-101).",
  "draft_reply": "Thank you for contacting Alpine Outdoor about your refund request for the duplicate item on order. We have received your request and noted that you ordered the item by mistake and that it has not been opened. Your request is being reviewed by our Fulfillment Support team, who will check the order details and the delivery information. To help with this review, please reply with the date the order was delivered and, if you have one, a photo of the unopened item and its packaging. We cannot confirm the outcome of your request until that review is complete. We will update you once a decision has been made.",
  "draft_case_note": "CS-5225: Customer requests refund for a duplicate outdoor clothing item ordered by mistake, reported unopened, $47, order date 2026-10-06, delivered. No evidence provided. Rule T1 fired (possible fulfillment error), routed to Fulfillment Support. Rule R8 not evaluable (prior_related_claims_90d unknown). Delivery date missing, so return window not confirmed under POL-RETURN. No refund or return label issued; pending Fulfillment Support review. Customer asked for delivery date and any photo of the unopened item. Confidence low."
}
```

## CS-5225 | fields_plus_simulated_message | v4 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5225",
  "issue_type": "return",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Exact delivery date (only order date 2026-10-06 and delivered status are provided)",
    "Verification of item condition (customer states one unit is unopened; not verified)",
    "Confirmation that the order record matches the duplicate purchase described"
  ],
  "customer_requested_outcome": "Refund for one unopened duplicate item from order AO-418225 (customer asks whether it can be returned for a refund)",
  "key_facts": [
    "Customer reports ordering the same item twice by mistake under order AO-418225",
    "Customer reports one unit is still unopened",
    "Order status: Delivered; order date 2026-10-06",
    "Purchase amount: $47 USD",
    "Channel: Chat; no supporting evidence provided",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown"
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN", "KB-101"],
  "confidence": "low",
  "needs_human_judgment_reason": "Routing to Fulfillment Support is mandatory under rule T1, but the customer describes a duplicate order placed by mistake, which may not be a fulfillment error; the representative should confirm the correct category. Eligibility depends on whether the order is within the 30-day standard online return window from delivery, which requires the exact delivery date. Item condition (unopened) is only customer-reported and unverified; the policy requires unused, resalable items with original tags or packaging where applicable. Rule R8 could not be evaluated because prior_related_claims_90d is unknown, so that check remains open. The approved sources do not cover duplicate-order-by-mistake returns specifically, so the outcome requires review under the applicable policy. No refund or return label can be confirmed from these sources.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about order AO-418225. I understand you ordered the same item twice by mistake and that one unit is still unopened. I have passed your request to our Fulfillment Support team, who will review your order and the return options that apply. I cannot confirm at this time whether a return or refund is available, and I am not able to issue a return label or refund in this chat. To help the review, please reply with the date your order was delivered and whether the unopened item still has its original tags or packaging. A team member will follow up with you once the review is complete.",
  "draft_case_note": "CS-5225: Customer reports accidentally ordering the same item twice (order AO-418225, $47, delivered, order date 2026-10-06). Customer states one unit is unopened; not verified. No evidence provided. Rule T1 fired and routed to Fulfillment Support; required approval Fulfillment Support. Rule R8 not evaluable (prior_related_claims_90d unknown). Sources: POL-RETURN, KB-101. Missing: exact delivery date, item condition verification, tags/packaging status. No return, refund, or label was offered or approved. Customer told the request is under review and asked for delivery date and packaging details. Confidence low: duplicate-order scenario not covered in approved sources; routing rule may not match case type."
}
```

## CS-5244 | fields_only | v4 | severity 5

route=Support Lead owner=Support Representative policy=Support Lead | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5244",
  "issue_type": "refund",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Delivery date (order date 2026-09-27 is provided; delivery date is not stated)",
    "Current condition of the item and how it was used beyond the single wash",
    "Supporting evidence of the product condition (none provided)",
    "Required rule-layer account information needed to complete the R8 check, which could not be evaluated"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Outdoor clothing purchase, order date 2026-09-27, status Delivered",
    "Purchase amount $55 USD",
    "Customer reports the item was washed once and tags were removed",
    "Customer requests a refund",
    "No evidence provided",
    "Rule R4 fired: return may be outside the 30-day window or the item may be used or its condition unclear, so no automatic approval and policy review is required",
    "Rule R8 could not be evaluated because required information is missing; the rule layer does not allow a guess"
  ],
  "rule_flags": ["R4"],
  "recommended_route": "Support Lead",
  "required_approvals": ["Support Lead"],
  "sources_cited": ["POL-RETURN", "KB-101", "KB-510"],
  "confidence": "low",
  "needs_human_judgment_reason": "The item has been washed and tags removed, which indicates use and may affect resalable condition under the return policy. Rule R4 fired, requiring Support Lead policy review, and the rule layer states there is no automatic approval. Delivery date and item condition details are missing. Rule R8 could not be evaluated due to missing information and must not be guessed. KB-510 does not allow a statement that washed or de-tagged items remain eligible for return. No approved source covers the outcome for this specific case, so a Support Lead should decide eligibility and any refund. Representative should not promise a refund or return label.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about your return request for your outdoor clothing order. I can see your order and that it was delivered. Your request has been referred to a team member who will review it under our return policy, including the timing of the return and the condition of the item. I am not able to confirm a refund or return label at this time, and no decision has been made yet. To help with the review, could you please share the date your order was delivered and any details about how the item has been used since delivery? Once the review is complete, you will be contacted with the outcome.",
  "draft_case_note": "CS-5244: Customer requests refund for outdoor clothing (order date 2026-09-27, delivered, $55). Customer reports item washed once and tags removed. No evidence provided. Rule R4 fired (possible outside-window return or used/unclear condition); routed to Support Lead for policy review, no automatic approval. R8 could not be evaluated due to missing information. Delivery date and item condition details requested. No refund or return label offered or promised. Sources: POL-RETURN, KB-101, KB-510. Confidence low."
}
```

## CS-5244 | fields_plus_simulated_message | v4 | severity 5

route=Support Lead owner=Support Representative policy=Support Lead | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5244",
  "issue_type": "return",
  "product_category": "Outdoor clothing (waterproof jacket)",
  "order_number_present": true,
  "missing_information": [
    "Exact delivery date, needed to confirm the 30-day return window",
    "Confirmation of the item's current condition, since it was washed and tags were removed",
    "Prior related claims in the last 90 days (rule R8 could not be evaluated)"
  ],
  "customer_requested_outcome": "Refund for a waterproof jacket (order AO-418244) that does not fit as hoped",
  "key_facts": [
    "Order AO-418244 was placed 2026-09-27 and shows as delivered; purchase amount is $55 USD.",
    "Customer reports the jacket was washed once and the tags were removed.",
    "Customer says the jacket does not fit the way they hoped.",
    "No evidence was provided.",
    "Rule R4 fired: the return may be outside 30 days or the item may be used or in unclear condition, so no automatic approval applies and policy review is required.",
    "Rule R8 could not be evaluated because prior_related_claims_90d is unknown.",
    "Per KB-510, return eligibility cannot be stated as continuing after washing or tag removal; it depends on policy and product condition."
  ],
  "rule_flags": ["R4"],
  "recommended_route": "Support Lead",
  "required_approvals": ["Support Lead"],
  "sources_cited": ["POL-RETURN", "KB-101", "KB-510", "NOTE-KNOWLEDGE-QUALITY"],
  "confidence": "low",
  "needs_human_judgment_reason": "The item was washed and the tags were removed, and the delivery date needed to confirm the 30-day window is not in the case. Rule R4 requires a Support Lead policy review, and no refund or return eligibility can be confirmed from the approved sources. Rule R8 could not be evaluated because prior claims data is missing. The sources do not state a standard return outcome for used items, so a representative must decide.",
  "draft_reply": "Thank you for reaching out about order AO-418244. I'm sorry the jacket didn't fit the way you hoped. Your return request is being reviewed by our Support Lead team, because the jacket has been washed and the tags have been removed, and those details affect how the return policy applies. I can't confirm whether this return or a refund is eligible at this time. A team member will review your order and reply with the outcome. Please keep the jacket and its packaging until you hear back. If you have your delivery confirmation or any other details about the jacket's condition, please share them so the review can be completed.",
  "draft_case_note": "CS-5244: Customer requests refund for waterproof jacket, order AO-418244 (ordered 2026-09-27, delivered, $55). Customer states item was washed once and tags removed; fit concern. No evidence provided. R4 fired (possible out-of-window or used/unclear condition); routed to Support Lead for policy review. R8 not evaluable (prior claims unknown). No refund, return label, or eligibility was confirmed or promised. Missing: exact delivery date, current item condition, prior claims data. Draft reply sent for representative review."
}
```

