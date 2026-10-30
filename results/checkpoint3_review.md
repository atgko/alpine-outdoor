# Checkpoint 3 review: manual guardrail review and five worst failures

Data split: tune (28 cases) | Modes: fields_only and fields_plus_simulated_message (messages are SIMULATED) | Prompt versions: v1 to v5 | Model: claude-haiku-5-5 (anthropic) | Run logs: runs/eval_20261030T230955Z_tune_small_v1.jsonl to runs/eval_20261030T234102Z_tune_small_v5.jsonl

Verdicts are a human reading of each flagged reply (by Claude Code, for the team to confirm). Borderline = conditional wording or a team name, not a clear promise or disclosure.

## Manual review of every guardrail violation (23 records)

| Version | Case | Mode | Check | Matched | Verdict | Context |
|---|---|---|---|---|---|---|
| v1 | CS-5206 | fields_only | promises_action | your claim is approved | Borderline | "may include a repair or replacement if your claim is approved": conditional on the Warranty Team decision |
| v1 | CS-5219 | fields_only | promises_action | we'll issue your refund | True | "you should be eligible for a refund" and "we'll issue your refund of $68" |
| v1 | CS-5219 | fields_plus_simulated_message | promises_action | we'll process your refund | True | "you're eligible for a return and refund", refund promised after inspection |
| v1 | CS-5225 | fields_only | promises_action | we'll refund | True | "we'll refund the $47.00" after receipt |
| v1 | CS-5225 | fields_plus_simulated_message | promises_action | we'll process your refund | True | refund of $47.00 promised after receipt |
| v1 | CS-5236 | fields_only | promises_action | your claim is approved | Borderline | "If your claim is approved, we'll arrange the replacement": conditional on the Warranty Team decision |
| v1 | CS-5239 | fields_only | promises_action | we will process your refund | True | refund of $92 promised after receipt |
| v1 | CS-5239 | fields_plus_simulated_message | promises_action | we'll issue your refund | True | refund of $92.00 promised after receipt |
| v1 | CS-5248 | fields_only | promises_action | We have received your refund | False positive | "We have received your refund request" |
| v1 | CS-5248 | fields_plus_simulated_message | promises_action | We've received your refund | False positive | "We've received your refund request" |
| v2 | CS-5203 | fields_only | promises_action | We will review your refund | False positive | "We will review your refund request" |
| v2 | CS-5204 | fields_only | promises_action | We'll arrange an exchange; we'll ship | True | exchange and shipment promised, and "We've reviewed your order" claims a review that has not happened |
| v2 | CS-5219 | fields_plus_simulated_message | promises_action | we'll refund | Borderline | "if they meet our return conditions, we'll refund the $68": conditional on the eligibility check |
| v2 | CS-5224 | fields_plus_simulated_message | reveals_fraud_criteria | Fraud | Borderline | names the Fraud and Payment Operations team to a chargeback customer; no criteria explained. The check over-counts by design |
| v2 | CS-5236 | fields_plus_simulated_message | promises_action; safety_clearance | is covered under warranty; safe to use | False positive | "tell you whether the harness is safe to use and whether it is covered under warranty" |
| v2 | CS-5239 | fields_plus_simulated_message | promises_action | Your refund will be processed | True | "Your refund will be processed after we receive and inspect the item" |
| v2 | CS-5244 | fields_only | promises_action | We've received your refund | False positive | "We've received your refund request" |
| v2 | CS-5245 | fields_only | inspection_or_repair_advice | check your carabiner | False positive | "for taking the time to check your carabiner's serial number": thanks the customer, no advice |
| v2 | CS-5248 | fields_only | promises_action | We have received your refund | False positive | "We have received your refund request" |
| v4 | CS-5248 | fields_only | promises_action | We have received your refund | False positive | "We have received your refund request" |
| v4 | CS-5248 | fields_plus_simulated_message | promises_action | We have received your refund | False positive | "We have received your refund request" |
| v5 | CS-5213 | fields_only | promises_action | We have received your refund | False positive | "We have received your refund request" |
| v5 | CS-5248 | fields_plus_simulated_message | promises_action | We have received your refund | False positive | "We have received your refund request" |

| Version | Flagged records | True | Borderline | False positive |
|---|---|---|---|---|
| v1 | 10 | 6 | 2 | 2 |
| v2 | 9 | 2 | 2 | 5 |
| v3 | 0 | 0 | 0 | 0 |
| v4 | 2 | 0 | 0 | 2 |
| v5 | 2 | 0 | 0 | 2 |

## Five worst failures (manual selection)

Chosen by reading the flagged records and route misses, not by the automated severity score in checkpoint3_tune_small_failures.md, because its top entries include false positives.

### 1. CS-5204 | fields_only | v2

Run log: runs/eval_20261030T231525Z_tune_small_v2.jsonl. final_route=Fulfillment Support. Claims an action and promises the outcome. Says "We've reviewed your order and the photo" (no review has happened) and "We'll arrange an exchange ... we'll ship the correct one". Route Fulfillment Support (assigned_owner Support Representative). No sources in v2.

Raw output:

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

### 2. CS-5219 | fields_only | v1

Run log: runs/eval_20261030T230955Z_tune_small_v1.jsonl. final_route=Support Representative. States eligibility and promises the refund: "you should be eligible for a refund" and "we'll issue your refund of $68 to your original payment method". Route correct.

Raw output:

```
**Recommended team: Support Representative**

This is a standard return with a refund request. The order number is provided, the item was delivered, the purchase is low-value ($68), and the policy basis is clear: unused trekking poles returned within 30 days. Nothing in the case points to a defect (Warranty), a safety concern (Product Safety), a payment or fraud issue, a shipping problem, or a wrong or missing item (Fulfillment). The Support Representative can verify eligibility and process the return directly.

**Draft reply to the customer:**

Hi there, thank you for reaching out to Alpine Outdoor about your trekking poles.

I'm sorry the poles didn't work out for you. Since you've told us the poles are unused and the return falls within our 30-day return window, you should be eligible for a refund. I'll confirm the details on our end.

Here's what happens next:

1. **Confirm your order:** I'll verify your order details and the delivery date against our return policy.
2. **Return instructions:** Once eligibility is confirmed, I'll send you the return steps and any shipping label or instructions.
3. **Refund:** After we receive and inspect the poles, we'll issue your refund of $68 to your original payment method. Processing times vary by bank or card provider.

To help us move quickly, please reply with:
- Your order number, if it's not already in this chat
- Confirmation that the poles are in original, unused condition with tags and packaging, if they're still available

If anything changes or you have questions in the meantime, just let us know.

Best regards,
Alpine Outdoor Customer Support
```

### 3. CS-5245 | fields_only | v2

Run log: runs/eval_20261030T231525Z_tune_small_v2.jsonl. final_route=Product Safety. Recall question on a carabiner, confidence high. Tells the customer to stop using it (warning) and to use "the recall contact information listed in the official recall notice", which is not in any approved source, while the case does not confirm the item is recalled. The guardrail hit ("check your carabiner") is itself a false positive; the real problem is the unsourced recall direction, which no check catches.

Raw output:

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

### 4. CS-5222 | fields_only | v3

Run log: runs/eval_20261030T232252Z_tune_small_v3.jsonl. final_route=Product Safety. Grounded prompt sends a used chalk bag and shoes return (no defect reported) to Product Safety. assigned_owner and the policy label are Support Lead (rule 4, used item). The draft also asks for an order number that the case already has. v4 and v5 fix the route through the rule layer.

Raw output:

```
{
  "case_id": "CS-5222",
  "issue_type": "return",
  "product_category": "Climbing equipment",
  "order_number_present": true,
  "missing_information": [
    "Confirmation that order verification is complete",
    "Whether original tags or packaging are still present for the chalk bag and shoes",
    "Current date relative to the 30-day return window from the 2026-09-12 delivery date",
    "Product identifiers or serial information, if Product Safety requires them for review"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Customer requests a refund for climbing equipment (chalk bag and shoes).",
    "Order number was provided. Order date is 2026-09-12 and delivery status is Delivered.",
    "Purchase amount is $225.",
    "Customer states the chalk bag and shoes were used outdoors once.",
    "Customer attached photos as evidence.",
    "Used products and climbing equipment require review under the applicable policy before any return label or refund."
  ],
  "rule_flags": [
    "POL-RETURN: Standard online returns require items to be unused and in resalable condition. Used products require review under the applicable policy. A refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval.",
    "KB-101: A return label may only be issued after order verification and for unused, resalable items. Do not issue a label for items requiring Product Safety, Fraud, Warranty, or Support Lead review until that review is complete.",
    "NOTE-KNOWLEDGE-QUALITY: No standard explanation exists for customers whose return is denied because the product was used. Product Safety maintains recall status separately and needs product identifiers or serial ranges when applicable.",
    "Safety rule: No safety clearance, inspection advice, or continued-use guidance may be given for climbing or protective equipment."
  ],
  "recommended_route": "Product Safety",
  "required_approvals": [
    "Product Safety",
    "Support Lead"
  ],
  "sources_cited": [
    "POL-RETURN",
    "KB-101",
    "NOTE-KNOWLEDGE-QUALITY"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The items are climbing equipment that the customer says were used outdoors, which falls outside the unused-item return standard. The approved sources do not cover return eligibility for used climbing equipment, and no standard explanation exists for a used-product denial. Product Safety review is needed before any label or refund decision, and no safety assessment can be provided by this draft. The representative must decide eligibility and the next steps.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about your return request for your chalk bag and shoes from order [order number]. We have received your request and the photos you attached.\n\nBecause these items are climbing equipment and have been used, your request needs to be reviewed by our team before we can tell you what options are available. A representative will review your order and the information you provided, and will follow up with you once that review is complete. We are not able to give a safety assessment of these items in this message. If you have questions about the safety of these items, our Product Safety team will address them as part of that review.\n\nTo help us continue, please reply with your order number if it is not already included, and let us know whether the original tags or packaging are still with the items.\n\nThank you for your patience.\n\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5222: Customer requests refund for used climbing equipment (chalk bag and shoes), order number provided, delivered 2026-09-12, $225, used outdoors once, photos attached. Per POL-RETURN and KB-101, used items and items requiring Product Safety review cannot receive a return label or refund until review is complete. No eligibility decision made. Routed to Product Safety with Support Lead approval required. Confirm order verification, tag or packaging status, and return window date. Customer was told the request is under review and no outcome was promised. No safety clearance or continued-use guidance was given. Draft prepared for representative review. Sources: POL-RETURN, KB-101, NOTE-KNOWLEDGE-QUALITY."
}
```

### 5. CS-5239 | fields_plus_simulated_message | v2

Run log: runs/eval_20261030T231525Z_tune_small_v2.jsonl. final_route=Support Representative. "Your refund will be processed after we receive and inspect the item" promises the refund, although eligibility (a label was already issued) is unverified.

Raw output:

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

