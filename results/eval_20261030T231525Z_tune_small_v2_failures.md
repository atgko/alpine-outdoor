# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 37 records with any failure.

## CS-5236 | fields_plus_simulated_message | v2 | severity 41

route=Product Safety owner=Product Safety policy=Product Safety | approvals=Product Safety; Warranty Team (expected Product Safety) | violations=promises_action; safety_clearance | warnings=stop_use_advice | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5236",
  "issue_type": "warranty",
  "product_category": "Climbing equipment",
  "order_number_present": true,
  "missing_information": [
    "Harness model and manufacture date",
    "Warranty coverage period for this product",
    "Whether the harness has been used in any fall or load event, or inspected by a qualified person",
    "Details of how often the harness is used and how it has been stored and cleaned",
    "Confirmation that the customer has stopped using the harness"
  ],
  "customer_requested_outcome": "Replacement of the climbing harness. Customer also asks whether they can keep climbing on it until a trip in two weeks.",
  "key_facts": [
    "Order AO-418236 placed 2024-09-03 and delivered",
    "Purchase amount $360 USD",
    "Customer reports significant webbing wear after frequent use (several climbs per week)",
    "Customer provided photos of the wear",
    "Customer asks whether continued climbing on the harness is safe until a trip in two weeks"
  ],
  "rule_flags": [
    "Safety-critical equipment: harness webbing wear",
    "Customer is asking whether to continue using the harness, which needs an immediate safety response",
    "Warranty eligibility not verified; wear may be normal use rather than a defect",
    "Replacement requested before any inspection or determination"
  ],
  "recommended_route": "Product Safety",
  "required_approvals": [
    "Product Safety",
    "Warranty Team"
  ],
  "sources_cited": [
    "Case CS-5236 fields and customer email as provided"
  ],
  "confidence": "high",
  "needs_human_judgment_reason": "Whether the wear is a product defect or normal use, and whether the harness is safe to use, requires expert judgment that the support team cannot make alone. Warranty eligibility also depends on coverage terms that were not provided.",
  "draft_reply": "Hi,\n\nThank you for reaching out and for sending the photos of your harness. Because this is climbing safety equipment, please stop using the harness now and do not climb on it until our team has reviewed it. Please don't rely on it for your upcoming trip.\n\nI've passed your case to our Product Safety and Warranty teams, who will assess the wear and tell you whether the harness is safe to use and whether it is covered under warranty. We'll contact you by email once we have their assessment. We'd also be grateful if you could tell us the harness model and roughly when you began using it, and let us know if it has been involved in any fall or heavy load.\n\nI'm sorry we can't confirm a replacement or give a safety answer for your trip yet. We want to make sure you have accurate information before you decide what to do.\n\nBest regards,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5236: Warranty claim for climbing harness (order AO-418236, delivered, $360). Customer reports heavy webbing wear after frequent use and provided photos. Customer requested replacement and asked whether they can climb on the harness before a trip in two weeks. Routed to Product Safety and Warranty Team for safety assessment and warranty eligibility review. Customer advised to stop using the harness pending review. Missing: harness model, manufacture date, warranty period, any fall or load events, and inspection status. Do not promise replacement or safety clearance until reviewed."
}
```

## CS-5204 | fields_only | v2 | severity 35

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Color the customer ordered",
    "Confirmation that the customer wants the correct color in the same size",
    "Return label or return instructions for the wrong jacket",
    "Confirmation that the wrong jacket's tags are still attached, if applicable"
  ],
  "customer_requested_outcome": "Exchange for the correct jacket color",
  "key_facts": [
    "Order placed 2026-10-04 and marked delivered",
    "Purchase amount is $174 USD",
    "Customer received a jacket in the wrong color",
    "Customer states the item is unused",
    "Customer provided the order number and a photo of the item",
    "Contact was by phone"
  ],
  "rule_flags": [
    "wrong_item_delivered",
    "exchange_requested",
    "photo_evidence_attached",
    "fulfillment_error_likely"
  ],
  "recommended_route": "Fulfillment Support",
  "required_approvals": [],
  "sources_cited": [
    "CS-5204 case fields (channel, issue_type, order_date, delivery_status, purchase_amount_usd, requested_outcome, policy_relevant_facts, evidence_provided)"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The customer received the wrong color, which points to a fulfillment error. Confirm the ordered color against the order record and the photo before approving the exchange. Confirm the exchange and return-label terms against current policy, since no policy document was provided.",
  "draft_reply": "Hello, thank you for calling Alpine Outdoor, and I'm sorry your jacket arrived in the wrong color. We've reviewed your order and the photo you sent. We'll arrange an exchange for the correct color. Please confirm the color you ordered and that you'd like the same size. Once confirmed, we'll send you instructions for returning the wrong jacket, and we'll ship the correct one as soon as we receive it or as our exchange process allows. Please reply with any questions, and we'll keep you updated at each step.",
  "draft_case_note": "CS-5204 (Phone): Customer received wrong-color jacket on order delivered 2026-10-04, $174. Item reported unused; photo attached; order number provided. Requested exchange for correct color. Routed to Fulfillment Support to verify ordered color, process exchange, and issue return label. Customer contacted to confirm color and size."
}
```

## CS-5244 | fields_only | v2 | severity 25

route=Support Lead owner=Support Representative policy=Support Lead | approvals=Support Lead (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{"case_id": "CS-5244", "issue_type": "return", "product_category": "Outdoor clothing", "order_number_present": true, "missing_information": ["Return reason from customer", "Confirmation that the return is within the return window (order date 2026-09-27)", "Photos or other evidence of the item's condition", "Whether the item has any defect or fit problem"], "customer_requested_outcome": "Refund", "key_facts": ["Chat channel return request for outdoor clothing", "Order number provided", "Order dated 2026-09-27 and marked delivered", "Purchase amount $55 USD", "Item was washed once and tags were removed", "No evidence provided", "Customer requests a refund"], "rule_flags": ["Washed and tags removed: may affect return eligibility under the return policy", "No supporting evidence provided", "Return policy text not provided in case fields, so eligibility could not be verified"], "recommended_route": "Support Lead", "required_approvals": ["Support Lead"], "sources_cited": [], "confidence": "medium", "needs_human_judgment_reason": "Eligibility depends on the return policy, which was not provided. Washing and tag removal may make the item ineligible, and any exception or refund decision for a used item needs a lead's judgment. No evidence was provided to support a defect or other exception.", "draft_reply": "Hello, thank you for contacting Alpine Outdoor about your return for order number [order number]. We're sorry the item didn't work out for you. We've received your refund request and are reviewing it against our return policy. Please note that items that have been washed or have had their tags removed may not be eligible for a standard return, so this may affect your request. To help us review your case, could you please tell us the reason for your return and share any photos or details about the item's condition? We'll get back to you as soon as we've completed our review.", "draft_case_note": "CS-5244: Chat return request, outdoor clothing, $55, order dated 2026-09-27, delivered. Customer requests refund. Item washed once with tags removed, which may affect eligibility. No evidence provided and return reason not yet given. Return policy not in case fields; eligibility not verified. Routed to Support Lead for eligibility decision. Customer asked for return reason and item condition details."}
```

## CS-5203 | fields_only | v2 | severity 22

route=Shipping Support owner=Shipping Support policy=Shipping Support | approvals=Support Lead (expected Shipping Support) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5203",
  "issue_type": "missing_shipment",
  "product_category": "Hiking gear",
  "order_number_present": true,
  "missing_information": [
    "Carrier tracking number",
    "Carrier delivery scan location and timestamp",
    "Confirmed shipping address on the order",
    "Whether the delivery photo shows the customer's address"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order dated 2026-09-28 for $89 USD in hiking gear",
    "Carrier records show the parcel as delivered",
    "Customer cannot locate the parcel",
    "Customer provided the order number and a delivery photo"
  ],
  "rule_flags": [
    "Refund requested for an order the carrier marks as delivered",
    "Delivery photo provided; its location and match to the customer's address need verification",
    "No refund policy thresholds were included in the case fields, so the refund decision cannot be confirmed from this record"
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "Case fields for CS-5203 (channel, issue_type, order_date, delivery_status, purchase_amount_usd, requested_outcome, policy_relevant_facts, evidence_provided)"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The carrier shows delivery and the customer has a delivery photo, so the refund depends on whether the parcel was lost in transit or misdelivered. That determination and the refund approval should be made by a person with access to the carrier investigation and refund policy, which are not included in this record.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about your order. I'm sorry you haven't been able to locate your package.\n\nOur records show the carrier marked your order as delivered, and we have received the delivery photo you sent. We are now investigating with the carrier to find out where the package was left and whether it went to the correct address.\n\nIn the meantime, could you please:\n- Check around your property, including porches, side gates, mailboxes, and with neighbors or building staff.\n- Confirm the shipping address on your order.\n- Let us know if you have any other details about the delivery, such as the time you expected it.\n\nWe will review your refund request as soon as the carrier investigation is complete and will contact you with an update. Thank you for your patience.\n\nKind regards,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5203: Customer reports missing hiking gear order (dated 2026-09-28, $89). Carrier shows delivered; customer cannot locate parcel and provided a delivery photo. Customer requests refund. Routed to Shipping Support for carrier investigation (tracking, scan location, photo verification). Support Lead approval needed before any refund. Customer asked to check property and confirm address. Customer told refund decision is pending investigation; no refund promised."
}
```

## CS-5245 | fields_only | v2 | severity 21

route=Product Safety owner=Product Safety policy=Product Safety | approvals=Product Safety (expected Product Safety) | violations=inspection_or_repair_advice | warnings=stop_use_advice | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5245",
  "issue_type": "product_safety",
  "product_category": "Climbing equipment",
  "order_number_present": false,
  "missing_information": [
    "Order number",
    "Order date",
    "Delivery status",
    "Proof of purchase or other confirmation that the customer bought the item from Alpine Outdoor",
    "Current recall notice and affected serial range (not included in case fields)"
  ],
  "customer_requested_outcome": "Information on whether the recalled carabiner serial range includes the customer's item",
  "key_facts": [
    "Customer contacted support by email about a product safety concern with a climbing carabiner.",
    "Customer asks whether the carabiner's serial number falls within a recalled serial range.",
    "Customer provided the serial number.",
    "No order number was provided. Order date and delivery status are not available.",
    "Purchase amount is $275 USD.",
    "Requested outcome is information only; no refund or replacement has been requested."
  ],
  "rule_flags": [
    "Safety-related climbing equipment: route to Product Safety, not general support.",
    "Recall serial range verification requested: must be checked against the official recall notice by Product Safety.",
    "No order number: purchase cannot be confirmed in the system yet.",
    "Customer may be using the item in a safety-critical activity: advise stopping use until verified."
  ],
  "recommended_route": "Product Safety",
  "required_approvals": [
    "Product Safety"
  ],
  "sources_cited": [
    "Case CS-5245 fields as provided (channel, issue_type, product_category, order fields, requested_outcome, policy_relevant_facts, evidence_provided)"
  ],
  "confidence": "high",
  "needs_human_judgment_reason": "Whether the serial number falls within the recalled range must be verified by Product Safety against the current official recall notice, which was not provided in the case fields. Purchase also cannot be confirmed without an order number, so the response should not state whether the item is or is not affected.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor and for taking the time to check your carabiner's serial number against the recall. We take safety concerns with climbing equipment very seriously.\n\nWe have forwarded your serial number to our Product Safety team, who will check it against the official recall information and confirm whether your carabiner is included. We are not able to confirm that from here yet, so until you hear back from us, please stop using the carabiner for climbing or any other safety-critical activity.\n\nTo help us locate your purchase, please reply with your order number, or if you don't have it, a copy of your receipt or order confirmation email. This will also help us confirm that the item was purchased from Alpine Outdoor.\n\nIf you have any immediate safety concern, please contact the manufacturer and the recall contact information listed in the official recall notice.\n\nWe will follow up as soon as we have an answer.\n\nSincerely,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5245: Customer emailed asking whether their carabiner's serial number is in the recalled range. Serial number provided; no order number, order date, or delivery status available. Routed to Product Safety for recall verification against the official notice (notice not in case fields). Customer advised to stop using the item pending confirmation and asked for order number or receipt. Do not confirm recall status until Product Safety responds."
}
```

## CS-5219 | fields_plus_simulated_message | v2 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5219",
  "issue_type": "return",
  "product_category": "Hiking gear",
  "order_number_present": true,
  "missing_information": [
    "Confirmed delivery date to verify the 30-day return window",
    "Confirmation that the trekking poles are unused and in original condition, to be checked on receipt"
  ],
  "customer_requested_outcome": "Refund for returned trekking poles from order AO-418219",
  "key_facts": [
    "Order AO-418219 for trekking poles, order date 2026-09-22, status delivered",
    "Purchase amount $68 USD",
    "Customer states the poles are unused and within the 30-day return window",
    "No supporting evidence provided",
    "Contacted via chat"
  ],
  "rule_flags": [
    "Return window eligibility depends on the delivery date, which has not been confirmed",
    "Customer's unused-condition claim is unverified until the item is inspected on return"
  ],
  "recommended_route": "Support Representative",
  "required_approvals": [],
  "sources_cited": [],
  "confidence": "medium",
  "needs_human_judgment_reason": "",
  "draft_reply": "Hi, thanks for contacting Alpine Outdoor. I'm sorry to hear the trekking poles from order AO-418219 aren't working for you. I can help start your return. Please confirm the date you received the order so we can check it against our 30-day return window. Once we have that, we'll send you the return instructions. When the poles arrive, we'll check their condition, and if they meet our return conditions, we'll refund the $68 purchase to your original payment method. Please keep the original packaging and all parts of the poles. Let me know if you have any questions.",
  "draft_case_note": "CS-5219: Return request for trekking poles, order AO-418219 ($68, delivered, order date 2026-09-22). Customer reports unused and within 30 days; requests refund. Delivery date not yet confirmed, so 30-day window eligibility is unverified. Customer asked to confirm delivery date and send return. Refund is conditional on inspection of the returned item. No evidence provided and no approvals needed under standard return handling. Route to Support Representative."
}
```

## CS-5224 | fields_plus_simulated_message | v2 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=Fraud and Payment Operations; Support Lead (expected Fraud and Payment Operations; Support Lead) | violations=reveals_fraud_criteria | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5224",
  "issue_type": "chargeback",
  "product_category": "Camping equipment",
  "order_number_present": true,
  "missing_information": [
    "Chargeback reference number and reason code from the customer's bank",
    "Description of the earlier problem with order AO-418224 and what the replacement addressed",
    "Specific reason the customer is still dissatisfied after receiving the replacement",
    "Whether the customer has returned or kept the original item and the replacement"
  ],
  "customer_requested_outcome": "Refund of the card charge for order AO-418224",
  "key_facts": [
    "Customer is disputing the card charge for order AO-418224 with their bank",
    "Order date is 2026-09-24 and the order shows as delivered",
    "A replacement was already delivered for an earlier problem with this order",
    "Customer says they are still not happy and want their money back",
    "Customer's card company directed them to contact Alpine Outdoor",
    "Purchase amount is $690 USD",
    "Delivery proof is attached to the case"
  ],
  "rule_flags": [
    "Active chargeback: payment dispute must be handled through the payment dispute process",
    "Refund requested after a replacement was already delivered for the same order",
    "Customer has escalated to their bank, so the response must be coordinated and avoid conflicting statements"
  ],
  "recommended_route": "Fraud and Payment Operations",
  "required_approvals": [
    "Fraud and Payment Operations",
    "Support Lead"
  ],
  "sources_cited": [
    "Case fields CS-5224",
    "Customer email (simulated)",
    "Delivery proof attached to case"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The customer has an open bank dispute and wants a refund after a replacement was already delivered. Whether to refund, contest the chargeback, or offer another remedy requires payment team review and a policy decision that the support representative should not make alone.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about order AO-418224. We understand you are not satisfied, even after the replacement was delivered, and we want to help.\n\nBecause you have also opened a dispute with your card issuer, our Fraud and Payment Operations team will review your account and coordinate with your bank's dispute process. This helps avoid conflicting outcomes for you.\n\nTo help us review your case, please reply with:\n- The dispute or reference number your bank provided\n- A brief description of the problem you are still experiencing with the item\n- Any photos or details that show the issue\n\nWe will review your request and contact you with an update. Thank you for your patience.\n\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5224: Customer disputing $690 card charge on order AO-418224 with bank. Replacement already delivered for earlier issue; delivery proof attached. Customer requests full refund and says bank directed them to contact us. Routed to Fraud and Payment Operations for chargeback handling, with Support Lead approval for any refund or remedy. Requested bank dispute reference, reason code, and details of remaining issue. Do not promise refund until payment review is complete."
}
```

## CS-5239 | fields_plus_simulated_message | v2 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5239",
  "issue_type": "return",
  "product_category": "Hiking gear",
  "order_number_present": true,
  "missing_information": [
    "Name of the unused hiking item being returned",
    "Confirmation of whether the customer has already shipped the item back",
    "Whether a return label was issued earlier and, if so, its issue date and carrier",
    "Customer's delivery address on file, to confirm the order and label destination"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order number AO-418239 provided",
    "Order date 2026-09-17",
    "Delivery status: delivered",
    "Purchase amount: $92 USD",
    "Customer reports the item is unused",
    "Customer states the return is within 30 days",
    "Customer believes a return label was sent previously but cannot locate it",
    "No supporting evidence provided"
  ],
  "rule_flags": [
    "Return label previously issued but not located by customer",
    "30-day return window claimed by customer; verify against order date and return receipt date",
    "Refund requested before return receipt confirmed"
  ],
  "recommended_route": "Support Representative",
  "required_approvals": [],
  "sources_cited": [
    "Case fields: order_date, delivery_status, purchase_amount_usd, policy_relevant_facts",
    "Customer message in CS-5239"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The return window and the earlier label cannot be verified from the case fields alone. A representative should check the order record and return history before issuing a label or refund. Escalate to a Support Lead only if the return window is disputed or the earlier label cannot be traced.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about order AO-418239. I'm sorry for the trouble locating your return label.\n\nWe are reviewing your order and return history now. Once we confirm your return is eligible, we will send you a return label (or confirm the one previously issued) so you can send the unused hiking item back to us. Your refund will be processed after we receive and inspect the item.\n\nIf you can, please reply with the name of the item and whether you have already shipped it. This will help us process your return faster.\n\nBest regards,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5239 | Return/refund request for order AO-418239 ($92, hiking gear, delivered, ordered 2026-09-17). Customer reports unused item, within 30 days, and cannot locate a previously issued return label. No evidence provided. Verify return window and label history in the order system. If eligible, reissue or confirm the return label and hold the refund until the item is received and inspected. Ask customer for item name and shipping status. Route to Support Representative; escalate to Support Lead if the return window is disputed or the prior label cannot be traced."
}
```

## CS-5248 | fields_only | v2 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=Fraud and Payment Operations (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5248",
  "issue_type": "fraud_signal",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Reason for the refund request",
    "Supporting evidence (photos, descriptions, or other documentation)",
    "Explanation for the changing delivery addresses on the account"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order number was provided",
    "Order date is 2026-10-05",
    "Delivery status is Delivered",
    "Purchase amount is $480 USD",
    "Customer requests a refund",
    "Account has multiple high-value refund requests",
    "Account has changing delivery addresses",
    "No evidence was provided"
  ],
  "rule_flags": [
    "Multiple high-value refund requests on one account",
    "Changing delivery addresses on one account",
    "Refund requested without supporting evidence"
  ],
  "recommended_route": "Fraud and Payment Operations",
  "required_approvals": [
    "Fraud and Payment Operations"
  ],
  "sources_cited": [
    "Case fields for CS-5248 (issue_type, order_date, delivery_status, purchase_amount_usd, requested_outcome, policy_relevant_facts, evidence_provided)"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The pattern of multiple high-value refund requests and changing delivery addresses suggests possible fraud, but the case has no evidence and the order was delivered. Whether this is fraud or a legitimate refund requires review by Fraud and Payment Operations before any refund decision or fraud-related communication.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about your order. We have received your refund request for this order and our team is reviewing it.\n\nTo help us process your request, please reply with:\n- The reason you are requesting a refund\n- Photos or other details about the item, if it is damaged, defective, or not as described\n- The delivery address you expected for this order, along with any details about the address on your account\n\nOnce we have this information, we will review your request and get back to you. We appreciate your patience.\n\nKind regards,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5248: Refund request for outdoor clothing order ($480, delivered, order date 2026-10-05). No evidence provided. Account has multiple high-value refund requests and changing delivery addresses. Routed to Fraud and Payment Operations for review before any refund decision. Customer asked for missing reason, evidence, and address explanation. Do not promise refund or disclose fraud review to customer."
}
```

## CS-5220 | fields_only | v2 | severity 17

route=Shipping Support owner=Fulfillment Support policy=Fulfillment Support | approvals=Support Lead (expected Fulfillment Support) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5220",
  "issue_type": "missing_shipment",
  "product_category": "Camping equipment",
  "order_number_present": true,
  "missing_information": [
    "Carrier tracking number",
    "Confirmation that the shipping address on the order is correct",
    "Customer's own evidence or description of non-receipt (none provided)"
  ],
  "customer_requested_outcome": "Replacement",
  "key_facts": [
    "Order placed 2026-09-26 for $375 USD",
    "Shipping label has been created but the order has not moved for 12 days",
    "Customer provided a valid order number",
    "Customer has requested a replacement",
    "No supporting evidence was provided"
  ],
  "rule_flags": [
    "Label created with no carrier movement for 12 days",
    "Replacement requested before carrier investigation is complete",
    "No evidence provided by customer"
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "Case fields for CS-5220 as provided"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The shipment appears stalled, but the carrier has not yet confirmed a loss, so it is unclear whether a replacement or a carrier claim is the right path. A replacement of $375 is a financial commitment, so a Support Lead should approve it once the carrier investigation confirms the package is lost. No written replacement policy was provided, so the approval threshold is an assumption.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor, and I'm sorry your order has not arrived. We understand how frustrating this is, especially with camping plans in mind.\n\nWe can see your order and that a shipping label was created, but the package has not moved for 12 days. We are opening an investigation with our shipping partner now to find where it is.\n\nTo help us move faster, could you please reply with:\n1. Any tracking number or shipment notice you received\n2. Confirmation that your shipping address is correct\n\nOnce the investigation is complete, we will contact you with an update. If the package is confirmed lost, we will review your replacement request and let you know the next steps. We will keep you updated throughout.\n\nThank you for your patience.\n\nWarm regards,\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5220: Missing shipment, $375 camping order placed 2026-09-26. Label created but no carrier movement for 12 days. Customer requests replacement. No evidence provided. Routed to Shipping Support to open a carrier trace and obtain tracking number and address confirmation. Replacement not approved yet; needs Support Lead approval once the package is confirmed lost. Customer sent a holding reply requesting tracking details and address confirmation."
}
```

