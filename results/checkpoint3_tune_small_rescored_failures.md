# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 99 records with any failure.

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

## CS-5206 | fields_only | v1 | severity 21

route=Warranty Team owner=Warranty Team policy=Warranty Team | approvals=- (expected Warranty Team) | violations=promises_action | warnings=stop_use_advice | api_ok=True schema_valid=None

```
**Recommended team: Warranty Team**

**Rationale:**
- The core issue is a warranty claim for a failed component (stove igniter) on a delivered order, with the customer requesting repair or replacement.
- The order number and video evidence are provided, so the Warranty Team can verify the purchase and assess the failure.
- Nothing in the case suggests a safety hazard, fraud, shipping damage, or a fulfillment error. If the video or customer reports a gas leak, fire, or other hazard, reroute to **Product Safety** immediately.

---

**Draft reply to customer:**

Subject: Re: Warranty Claim for Your Camp Stove (Case CS-5206)

Hi there,

Thank you for contacting Alpine Outdoor, and for sending the video of your stove's igniter. I'm sorry to hear it stopped working, especially after your camping trips.

I've forwarded your claim to our Warranty Team, who will review your order, the video, and the warranty terms that apply to your purchase. They will contact you at this email address with their findings and the next steps, which may include a repair or replacement if your claim is approved.

In the meantime, please stop using the stove until the warranty team has reviewed the case. If you notice any gas smell, leak, or other unusual behavior, please stop using it right away and let us know.

Thank you for your patience. We'll be in touch soon.

Best regards,
Alpine Outdoor Customer Support
Case Reference: CS-5206
```

## CS-5236 | fields_only | v1 | severity 21

route=Product Safety owner=Product Safety policy=Product Safety | approvals=- (expected Product Safety) | violations=promises_action | warnings=stop_use_advice | api_ok=True schema_valid=None

```
**Recommended team: Product Safety**, with the Warranty Team handling the replacement once Product Safety has reviewed the harness.

**Reasoning:** This is a warranty claim, but the product is a climbing harness and the reported problem is webbing wear. Webbing is a load-bearing fall-protection component, so the harness may be unsafe to use until someone qualified has inspected the photos. Product Safety should decide whether the wear is normal use or a defect that could affect safety, and whether the customer should stop using the harness. That determination then drives the warranty decision. The Warranty Team should take over for the replacement.

---

**Draft reply to customer**

Subject: Re: Warranty claim for your climbing harness (Case CS-5236)

Hi [Customer Name],

Thank you for contacting Alpine Outdoor and for sending photos of the wear on your harness. We're sorry you've run into this, especially with a product you rely on for climbing.

Because this is a climbing harness and the wear is on the webbing, which supports your weight during a fall, we're treating your claim as a safety review. Until we've completed that review, please **stop using the harness** and store it somewhere it won't be used by mistake. We know that's not what you want to hear, and we'll move as quickly as we can.

Here's what happens next:

1. **Safety review:** Our product safety team will examine your photos and the harness details to assess the wear.
2. **Warranty decision:** Once the review is complete, we'll confirm whether the harness qualifies for a replacement under our warranty policy and let you know the outcome.
3. **Replacement:** If your claim is approved, we'll arrange the replacement and share shipping details.

To help the review go faster, could you reply with:
- The model name and size of the harness
- The serial or lot number, if it's printed on a tag or on the harness
- A short description of how often you've been using it and in what conditions (for example, outdoor or indoor climbing, and roughly how many sessions)

We'll follow up within [timeframe]. If you have any questions in the meantime, reply to this email.

Thank you for your patience, and for helping us keep climbers safe.

Best regards,
[Agent Name]
Alpine Outdoor Customer Support
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

## CS-5219 | fields_only | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

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

## CS-5219 | fields_plus_simulated_message | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Support Representative**

This is a standard return. The customer reports unused trekking poles, delivery is confirmed, the order number is provided, the purchase is $68, and the request falls within the 30-day window. No safety concern, fraud signal, shipping problem, or warranty defect is mentioned, so no specialist team is needed. One note for the representative: the case has no supporting evidence, so they should verify the order and delivery date in the system before approving the refund.

**Draft reply to the customer:**

Hi there,

Thanks for reaching out about order AO-418219. I'm sorry to hear the trekking poles didn't work out for you.

Based on your message, the poles are unused and the order is within our 30-day return window, so you're eligible for a return and refund. I'm going to verify the order details on our end and start the return.

To complete the return, please:

1. Keep the trekking poles unused and in their original packaging if possible.
2. Include all original items and any included accessories or tags.
3. Follow the return instructions I'll send you, including the shipping label or return method for your order.

Once we receive and inspect the poles, we'll process your refund to your original payment method. I'll make sure you receive a confirmation when the refund is issued.

If you have any questions in the meantime, just reply here.

Best regards,
Alpine Outdoor Support
```

## CS-5225 | fields_only | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Support Representative**

This is a standard refund request. The order number is provided, the item was delivered, the customer says it was an unopened duplicate, and the amount is low ($47). No warranty, safety, shipping, payment-fraud, or fulfillment problem is reported. A Support Representative can verify the order and start the return and refund. Escalate to the Support Lead only if the order falls outside the return window or the customer disputes eligibility.

**Draft reply to the customer:**

Hi there,

Thank you for reaching out, and I'm sorry to hear you received a duplicate of an item by mistake. I can help with that.

I've noted that you ordered the item twice by mistake and that the duplicate is unopened. I'm looking up order [order number] now to confirm it's eligible for a refund under our return policy. Once that's confirmed, I'll send you return instructions for the unopened item.

After we receive the item and confirm it's in its original, unopened condition, we'll refund the $47.00 to your original payment method. Refunds typically take [X–Y business days] to appear, depending on your bank or card issuer.

If you have any questions in the meantime, just reply here.

Thanks for your patience,
[Agent name]
Alpine Outdoor Customer Support

*Before sending, confirm the return window and refund timeline from current policy and fill in the bracketed placeholders.*
```

## CS-5225 | fields_plus_simulated_message | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Support Representative**

This is a routine refund request. The customer ordered a duplicate by mistake, the item is unopened, the order number is provided, and the amount is low ($47). Nothing points to a safety defect, warranty claim, fraud, shipping failure, or fulfillment error, so none of the specialist teams are needed. Escalate to the Support Lead only if the return falls outside the standard return window or the customer disputes the outcome.

**Draft reply to customer:**

> Hi there,
>
> Thanks for reaching out, and no problem at all. Duplicate orders happen easily.
>
> Since the item is still unopened, you're likely eligible for a return and refund for that duplicate. Here's how to proceed:
>
> 1. Keep the duplicate item in its original, unopened packaging, with any tags still attached.
> 2. Reply to this chat with the order number (AO-418225) and confirm that you'd like to return the second unit.
> 3. We'll send you the return instructions and a prepaid label if one applies to your order.
>
> Once we receive the item and confirm it's in unopened condition, we'll process your refund of $47.00 to your original payment method. Refunds typically take [X–Y business days] to appear after processing, depending on your bank.
>
> Please keep your original item and order confirmation in case you need them. If you have any other questions, just let us know.
>
> Best regards,
> Alpine Outdoor Customer Support

*Note for the agent: Before sending, confirm the return window for this order date (2026-10-06) and the refund timeline, and replace the bracketed placeholder with the correct figures.*
```

## CS-5239 | fields_only | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Support Representative**

This is a standard return with a clear refund request, a low purchase amount ($92), no safety or fraud indicators, and a policy-compliant condition (unused, within 30 days). A Support Representative can verify the return status and process the refund. Escalate to **Shipping Support** if the customer confirms they shipped the item using the previously issued label and the return was never received.

**Draft reply to customer:**

Subject: Re: Your Return Request (Case CS-5239)

Hi there,

Thank you for contacting Alpine Outdoor, and I'm sorry the return has taken this long to resolve.

I've reviewed your request. Your item is eligible for a refund because it is unused and was returned within our 30-day return window. I can see that a return label was previously issued for this order.

To move your refund forward, could you please let me know:

1. Whether you have already shipped the item back using the return label, and if so, the tracking number.
2. If you have not shipped it yet, whether the label is still working or whether you'd like us to send you a new one.

Once we confirm the return has been received and inspected, we will process your refund of $92 to your original payment method.

Thank you for your patience. Please reply to this email if you have any questions.

Best regards,
Alpine Outdoor Customer Support
```

