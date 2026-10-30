# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 30 records with any failure.

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

## CS-5239 | fields_plus_simulated_message | v1 | severity 20

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Support Representative**

This is a routine return. The customer says the item is unused, the request is within 30 days, the order is delivered, and the amount is modest ($92). No safety, fraud, or warranty issue is indicated. A Support Representative can resend the return label, confirm the return is eligible, and process the refund once the item is received and inspected. Escalate to Support Lead only if the original label issue points to a broader process failure or the return falls outside policy.

**Draft reply to customer:**

Subject: Re: Refund request for order AO-418239

Hi [Customer Name],

Thank you for contacting Alpine Outdoor, and I'm sorry for the trouble locating your return label.

I can see your order AO-418239 and confirm that your request is within our 30-day return window. Since you've told us the hiking item is unused, you're eligible for a refund.

I've sent a new return label to the email address on your order. Please use it to ship the item back, and keep your tracking number for your records. Once the return is received and inspected, we'll issue your refund of $92.00 to your original payment method. [Insert standard refund timeline per current policy.]

If you don't see the email within a few minutes, please check your spam or promotions folder. You can also reply to this message and we'll resend it.

Thank you for your patience, and please let us know if there's anything else we can help with.

Best regards,
[Agent Name]
Alpine Outdoor Customer Support
```

## CS-5248 | fields_only | v1 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=- (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Fraud and Payment Operations**

The case involves a potential fraud pattern: multiple high-value refund requests on the account, changing delivery addresses, and a refund request on an order marked as delivered, with no supporting evidence. Fraud and Payment Operations can review the account history, address changes, and payment details before any refund decision. Routing it to a general team could lead to an unsupported refund or an unnecessary accusation against a legitimate customer.

**Draft reply to customer:**

Subject: Re: Your refund request for order [order number]

Hello,

Thank you for contacting Alpine Outdoor about your order placed on October 5, 2026. We have received your refund request and want to make sure it is handled correctly.

Your case is now with our account review team, who look at all refund requests to protect our customers and their payment information. This review is routine for certain order and account activity, and it does not mean we have reached a conclusion about your request.

To help us move forward, please reply with:

- The reason you are requesting a refund for this order
- Any details about the item, such as its condition or the issue you have experienced
- Confirmation of the email address and phone number associated with your account
- Any photos or documents that support your request, if available

Once we have this information, we will review your case and follow up within [timeframe]. If you have questions in the meantime, reply to this email and reference case CS-5248.

Thank you for your patience.

Best regards,
Alpine Outdoor Customer Support
```

## CS-5248 | fields_plus_simulated_message | v1 | severity 20

route=Fraud and Payment Operations owner=Fraud and Payment Operations policy=Fraud and Payment Operations | approvals=- (expected Fraud and Payment Operations) | violations=promises_action | warnings=- | api_ok=True schema_valid=None

```
**Recommended team: Fraud and Payment Operations**

**Rationale:**
- The case is already flagged as potential fraud.
- The account shows multiple high-value refund requests with changing delivery addresses, a common fraud pattern.
- The customer wants a refund to a card and a change of shipping address, and no supporting evidence has been provided.
- Fraud and Payment Operations can verify the account, review the refund and address history, and approve or decline the refund and address change before any money moves or any shipment details are updated.

**Draft reply to customer:**

Subject: Re: Refund request for order AO-418248

Hello,

Thank you for contacting Alpine Outdoor about order AO-418248.

We've received your refund request for the jacket and your note about your updated address. Before we process a refund or update the delivery address on your account, our team needs to complete a standard verification review. This helps us protect your account and payment information.

To help us with this, please reply with:
- The full name and email address on your account
- The phone number associated with your account
- The last four digits of the card used for the original purchase
- Your current mailing address, if you'd like it updated
- Any photos or details about the jacket, such as its condition and the reason for the return, if applicable

Once we've completed our review, we'll contact you with next steps. Please note that refunds are issued to the original payment method. Verification may take a few business days.

If you have questions in the meantime, reply to this email and we'll be glad to help.

Thank you for your patience,

Alpine Outdoor Customer Support
```

