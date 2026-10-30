# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 23 records with any failure.

## CS-5220 | fields_only | v3 | severity 17

route=Shipping Support owner=Fulfillment Support policy=Fulfillment Support | approvals=Support Lead (expected Fulfillment Support) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5220",
  "issue_type": "shipping_delay",
  "product_category": "Camping equipment",
  "order_number_present": true,
  "missing_information": [
    "Current carrier tracking status and last scan location (the order is listed as 'Label created' with no movement reported)",
    "Current date, needed to confirm the 12-day no-movement period",
    "Approved delivery estimate for this shipment (not covered in approved sources)",
    "Outcome of any delivery investigation (none is open per the case fields; the order has not been marked delivered)",
    "Any evidence from the customer (none provided)"
  ],
  "customer_requested_outcome": "Replacement",
  "key_facts": [
    "Order date is 2026-09-26.",
    "Delivery status is 'Label created'. The package has not been marked delivered.",
    "The order has not moved for 12 days, according to the policy-relevant facts.",
    "Purchase amount is $375.",
    "The customer requested a replacement. No evidence was provided.",
    "An order number was provided."
  ],
  "rule_flags": [
    "POL-SHIPPING: Delayed shipments allow representatives to communicate current carrier status and an approved delivery estimate. A replacement is not promised in this case.",
    "POL-SHIPPING: Cases with a high order value require the appropriate escalation. The sources do not define a dollar threshold, so the $375 amount needs review.",
    "KB-205: Replacements or refunds require the result of the investigation and any required approval. KB-205 applies to orders marked delivered but reported missing. This order is not marked delivered, so the delivery investigation step may not apply yet. Shipping Support should confirm this.",
    "Replacement approval is not covered in approved sources beyond the requirement for the investigation result and any required approval."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "POL-SHIPPING",
    "KB-205"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The order has not been marked delivered, so this may be a shipping delay rather than a missing-delivered case. KB-205 covers orders marked delivered but reported missing, so its investigation requirement may not apply. Confirming the current carrier status and whether the 12-day no-movement period is accurate requires Shipping Support. The sources do not define the replacement approval path or the high-value escalation threshold for a $375 order. The customer has provided no evidence. A representative should decide on any replacement after these checks.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about your order. We have your order number and are reviewing the current status of your shipment with our shipping team. We understand you are concerned that the package has not moved for some time.\n\nWe cannot confirm a replacement at this time. Our team is checking the carrier status and will review your request once that information is available. We will follow up with you as soon as we have an update.\n\nIf you have any tracking details or other information about the shipment, please reply with them so we can include them in our review.\n\nThank you for your patience.\n\nAlpine Outdoor Customer Support",
  "draft_case_note": "CS-5220: Customer reports missing shipment for camping equipment, $375, order dated 2026-09-26. Status is Label created with no movement for 12 days per case facts. Customer requests replacement; no evidence provided. Not marked delivered, so KB-205 delivery investigation may not apply. Routed to Shipping Support to check carrier status and confirm the shipping state. Support Lead approval needed for any replacement decision. Confidence low: replacement approval path and high-value threshold not covered in approved sources. Draft reply sent with no replacement promised; asked customer for any tracking details."
}
```

## CS-5220 | fields_plus_simulated_message | v3 | severity 17

route=Shipping Support owner=Fulfillment Support policy=Fulfillment Support | approvals=Shipping Support (expected Fulfillment Support) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5220",
  "issue_type": "shipping_delay",
  "product_category": "Camping equipment",
  "order_number_present": true,
  "missing_information": [
    "Carrier tracking number and current carrier scan history",
    "Confirmation that the shipping address on the order is correct",
    "Approved delivery estimate for the order (not covered in approved sources)",
    "Whether the package has been scanned by the carrier since the label was created",
    "Result of any delivery investigation, which is required before a replacement can be considered"
  ],
  "customer_requested_outcome": "Replacement, because the order has shown 'label created' with no movement for 12 days and the customer is traveling soon.",
  "key_facts": [
    "Order AO-418220, placed 2026-09-26, purchase amount $375 USD.",
    "Tracking has shown 'label created' for 12 days with no movement, as reported by the customer.",
    "The customer has a trip coming up and needs the camping gear soon.",
    "No evidence was provided with the case.",
    "The package is not marked delivered, so it is not a missing-delivered case."
  ],
  "rule_flags": [
    "POL-SHIPPING: For a delayed shipment, representatives may communicate current carrier status and an approved delivery estimate. Only share what the carrier status shows.",
    "POL-SHIPPING: Address discrepancies, repeated missing shipment claims, or unusually high order value require the appropriate escalation. None is confirmed here, so the representative should check whether any apply.",
    "KB-205: A delivery investigation is required for orders marked delivered but reported missing. This order is not marked delivered, so KB-205 is referenced only for its rule that replacements require the investigation result and any required approval.",
    "Replacement decisions require the result of an investigation and any required approval. No replacement may be promised in the reply."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Shipping Support"
  ],
  "sources_cited": [
    "POL-SHIPPING",
    "KB-205"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The package is not marked delivered, so the delivered-but-missing path in KB-205 does not directly apply. Approved sources do not state how long a 'label created' status may remain before escalation, and the case has no carrier scan history or evidence. The customer is asking for a replacement, which requires an investigation result and approval that do not yet exist. A representative should confirm the carrier status and address and decide whether the case needs Shipping Support review or other escalation, including whether the order value meets any escalation threshold.",
  "draft_reply": "Hello,\n\nThank you for contacting Alpine Outdoor about order AO-418220, and I'm sorry for the worry this has caused, especially with your trip coming up.\n\nI can see your request has been received. The tracking information you describe shows a label created but no movement for 12 days. I'm passing your case to our shipping team to check the carrier status, confirm the shipping address on the order, and review the shipment. We will reply once that review is complete.\n\nI'm not able to confirm a replacement or a refund at this time. Any decision on a replacement will depend on the outcome of that review. I'm also not able to give a delivery estimate beyond what our team can confirm after checking.\n\nThank you for your patience.\n\nAlpine Outdoor Support",
  "draft_case_note": "CS-5220 / Order AO-418220. Customer reports tracking has shown 'label created' with no movement for 12 days. Order placed 2026-09-26, $375. Customer requests replacement and has a trip soon. No evidence provided. Order is not marked delivered, so KB-205 delivered-but-missing path does not directly apply. Per POL-SHIPPING, shared only that the case is under shipping review. No replacement, refund, or delivery estimate was promised. Routed to Shipping Support to check carrier scan history, confirm shipping address, and assess whether escalation applies. Replacement requires investigation result and approval. Confidence medium. Representative to review before sending."
}
```

## CS-5204 | fields_only | v3 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Ordered jacket color and the color received, as confirmed in the order record",
    "Confirmation that the item is unused, resalable, and has original tags or packaging, beyond the customer's statement and attached photo",
    "Inventory availability for the requested color or size, not covered in approved sources and to be checked in the authorized system"
  ],
  "customer_requested_outcome": "Exchange",
  "key_facts": [
    "Phone contact about an incorrect order for outdoor clothing",
    "Order date 2026-10-04; delivery status is Delivered",
    "Purchase amount $174",
    "Customer reports receiving the wrong jacket color",
    "Customer reports the item is unused",
    "Photo evidence attached",
    "Order number was provided"
  ],
  "rule_flags": [
    "Fulfillment errors may be corrected through the authorized replacement or exchange workflow after order verification (POL-RETURN).",
    "Exchanges for a different color may be offered for eligible unused items, subject to inventory availability (POL-RETURN).",
    "Eligibility for exchange depends on the item being unused and in resalable condition (POL-RETURN).",
    "Standard online purchases require the 30-day window from delivery, plus original tags or packaging where applicable (POL-RETURN).",
    "Exceptions and condition questions require review under the applicable policy. No refund may be issued until the authorized workflow confirms eligibility (POL-RETURN)."
  ],
  "recommended_route": "Fulfillment Support",
  "required_approvals": [
    "Fulfillment Support"
  ],
  "sources_cited": [
    "POL-RETURN"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The customer reports the wrong color and an unused item, and a photo is attached. Order verification, the actual color shipped versus ordered, item condition, tags or packaging, and inventory availability have not been confirmed in the approved sources or systems. A representative should verify these before any exchange path is considered.",
  "draft_reply": "Thank you for calling Alpine Outdoor and for sending the photo of the jacket you received. I'm sorry the color was not what you ordered. I have noted your report that the jacket is unused. Our team will verify your order details and the item we shipped. They will also check whether the color you need is available. Could you confirm whether the jacket still has its original tags or packaging? A representative will contact you with the next steps once the review is complete.",
  "draft_case_note": "CS-5204: Customer reports wrong jacket color received on an order delivered on record, order dated 2026-10-04, purchase amount $174. Customer states the item is unused and provided a photo. Customer requests exchange. Routed to Fulfillment Support to verify the order, the color shipped versus ordered, item condition, tags or packaging, and inventory availability under the authorized fulfillment exchange workflow (POL-RETURN). No exchange, refund, or return label has been approved or promised. Customer told a representative will follow up."
}
```

## CS-5204 | fields_plus_simulated_message | v3 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5204",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Order verification for AO-418204 in the authorized system",
    "Confirmation that the blue jacket is available in inventory for exchange",
    "Confirmation that the orange jacket is unused and has its original tags or packaging, where applicable",
    "Representative review of the attached photo against the order record"
  ],
  "customer_requested_outcome": "Exchange the orange rain jacket for the blue rain jacket ordered on AO-418204",
  "key_facts": [
    "Customer ordered a blue rain jacket (order AO-418204) and received an orange one.",
    "Order date is 2026-10-04 and the order shows as delivered.",
    "Customer states the item is unused.",
    "A photo was attached to the case.",
    "Purchase amount is $174.",
    "Channel is phone."
  ],
  "rule_flags": [
    "Fulfillment errors may be corrected through the authorized replacement or exchange workflow after order verification (POL-RETURN).",
    "Exchanges for a different color may be offered for eligible unused items, subject to inventory availability (POL-RETURN).",
    "A refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval (POL-RETURN).",
    "Items that are used, damaged, or outside the standard window require review under the applicable policy (POL-RETURN). Current facts do not indicate these conditions, but the item condition still needs verification."
  ],
  "recommended_route": "Fulfillment Support",
  "required_approvals": [
    "Fulfillment Support"
  ],
  "sources_cited": [
    "POL-RETURN"
  ],
  "confidence": "medium",
  "needs_human_judgment_reason": "The case is a wrong-color fulfillment error, which the policy routes through the authorized exchange workflow after order verification. Item condition (unused, tags present) is customer-reported and not yet verified, and blue jacket inventory is not confirmed. A representative must verify these before any exchange can be offered.",
  "draft_reply": "Thank you for contacting Alpine Outdoor and for sending the photo. I'm sorry you received the orange jacket instead of the blue one you ordered. I can see that you'd like to exchange it for the blue jacket on order AO-418204. Your request will be sent to our fulfillment team, who will verify the order, review the photo, check the condition of the jacket, and confirm whether the blue jacket is available for exchange. I can't confirm the exchange until that review is complete, but the team will follow up with you. Could you please confirm that the jacket has its original tags or packaging, if you still have them?",
  "draft_case_note": "CS-5204: Customer reports receiving orange rain jacket instead of blue on order AO-418204 (delivered, order date 2026-10-04, $174). Customer states item is unused and provided a photo. Customer requests exchange for blue jacket. Routed to Fulfillment Support for order verification, photo review, condition check (unused, tags/packaging), and blue jacket inventory check under the fulfillment error exchange workflow (POL-RETURN). No exchange approved or promised; customer told the team will follow up. Confidence medium pending verification."
}
```

## CS-5205 | fields_only | v3 | severity 15

route=Product Safety owner=Support Representative policy=Support Representative | approvals=Product Safety (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5205",
  "issue_type": "product_question",
  "product_category": "Climbing equipment",
  "order_number_present": false,
  "missing_information": [
    "Order number or order lookup details",
    "Harness product name, model, or identifier",
    "Order date and delivery status (not available)",
    "Whether the customer intends the harness for a child climbing or for another use (not covered in approved sources)",
    "Youth sizing or fit guidance for this harness model (not covered in approved sources)"
  ],
  "customer_requested_outcome": "Information on whether the harness fits a youth size",
  "key_facts": [
    "Channel: Chat",
    "Customer asks whether a harness fits a youth size",
    "Product category is climbing equipment, which is protective and safety equipment",
    "Purchase amount: 159 USD",
    "No order number was provided",
    "Order date and delivery status are not available",
    "No order lookup is possible without the order number or lookup details"
  ],
  "rule_flags": [
    "Climbing, protective, and safety equipment questions with a potential injury risk require Product Safety review (POL-WARRANTY-SAFETY).",
    "Support staff must not provide safety clearance, inspection advice beyond approved guidance, or a final decision for climbing or protective equipment (POL-WARRANTY-SAFETY, KB-427).",
    "Do not advise on use, fit, or inspection of climbing equipment beyond approved guidance (KB-427).",
    "No order number provided: list in missing_information and request order lookup details in the reply."
  ],
  "recommended_route": "Product Safety",
  "required_approvals": [
    "Product Safety"
  ],
  "sources_cited": [
    "POL-WARRANTY-SAFETY",
    "KB-427",
    "NOTE-KNOWLEDGE-QUALITY"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The customer asks about youth sizing for a climbing harness, which is a safety-sensitive fit question. Approved sources do not cover youth fit or sizing for this product, so the representative cannot answer it from the knowledge base. Product Safety review is needed before any fit guidance is given. The order number is also missing, so the product model cannot be confirmed.",
  "draft_reply": "Thank you for your question about whether this harness fits a youth size. Because this is climbing equipment and fit affects safety, I can't confirm fit or suitability from our current information. I've referred your question to our Product Safety team for review. To help locate your order and the correct product details, please send your order number or any order lookup details you have, such as the email address or billing name used at purchase, and the exact harness name or model. Once we have that information, a representative will follow up with you.",
  "draft_case_note": "CS-5205 (Chat): Customer asks whether a climbing harness fits a youth size. Climbing/protective equipment fit question is not covered in approved sources (KB-427, POL-WARRANTY-SAFETY). No fit, sizing, safety clearance, or inspection advice given. Routed to Product Safety for review. No order number provided; requested order lookup details and product model from customer. Order date and delivery status not available. Purchase amount 159 USD. Confidence low; needs Product Safety judgment on youth fit."
}
```

## CS-5205 | fields_plus_simulated_message | v3 | severity 15

route=Product Safety owner=Support Representative policy=Support Representative | approvals=Product Safety (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5205",
  "issue_type": "product_question",
  "product_category": "Climbing equipment",
  "order_number_present": false,
  "missing_information": [
    "Order number (not provided; no order is referenced as this is a pre-purchase question)",
    "Specific harness model name or product identifier",
    "Youth or child sizing specifications for the harness (not covered in approved sources)"
  ],
  "customer_requested_outcome": "Information on whether the climbing harness is available in a size that fits a 12-year-old, before purchase.",
  "key_facts": [
    "Customer is asking a pre-purchase question about a climbing harness priced at $159.",
    "Customer asks whether a size suitable for a 12-year-old is available.",
    "No order exists yet and no order number was provided.",
    "The approved sources do not contain harness sizing or youth fit information.",
    "The question concerns fit of climbing and safety equipment for a child."
  ],
  "rule_flags": [
    "Rule 1: Sizing and youth fit information is not covered in approved sources, so it cannot be stated.",
    "Rule 3: Climbing and safety equipment fit guidance cannot be given by support staff; no safety clearance may be provided.",
    "KB-427 and POL-WARRANTY-SAFETY: Climbing and protective equipment concerns are routed to Product Safety; this is a fit question, not a reported defect, but it involves safety equipment for a minor.",
    "Rule 9: No order number is available, so order lookup details are requested in the reply."
  ],
  "recommended_route": "Product Safety",
  "required_approvals": [
    "Product Safety"
  ],
  "sources_cited": [
    "POL-WARRANTY-SAFETY",
    "KB-427"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "Approved sources do not cover harness sizing or youth fit. The question concerns whether safety equipment fits a child, which requires Product Safety review rather than a support answer. No order exists yet, so there is no order record to check.",
  "draft_reply": "Hi, thank you for reaching out before your purchase. I don't have approved information about whether this harness comes in a size that fits a 12-year-old, and I don't want to guess on safety equipment. I've passed your question to our Product Safety team so they can review it and follow up with you. If you have a specific harness model name or product ID, please share it so we can point them to the right product. If you already have an order, please send the order number so we can look it up.",
  "draft_case_note": "Pre-purchase chat question from customer asking whether the $159 climbing harness comes in a size suitable for a 12-year-old. No order number provided; no order exists per customer context. Sizing/youth fit not covered in approved sources (KB-427, POL-WARRANTY-SAFETY). No safety clearance or fit advice given. Routed to Product Safety for review. Customer asked to provide model name or product ID and any order number. Low confidence; no action taken or promised."
}
```

## CS-5210 | fields_only | v3 | severity 15

route=Shipping Support owner=Support Representative policy=Support Representative | approvals=Shipping Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5210",
  "issue_type": "missing_shipment",
  "product_category": "Outdoor clothing",
  "order_number_present": false,
  "missing_information": [
    "Order number",
    "Order date",
    "Delivery status and carrier tracking status",
    "Shipping address on file",
    "Customer contact details or other order lookup identifiers",
    "Any evidence that the package was not received (for example, carrier notice or photos of the delivery location)"
  ],
  "customer_requested_outcome": "Replacement",
  "key_facts": [
    "Customer reports the package never arrived.",
    "Customer cannot locate the order number.",
    "No order date or delivery status is available.",
    "Purchase amount is $112 USD.",
    "No evidence has been provided."
  ],
  "rule_flags": [
    "KB-205: For a missing package, confirm the shipping address and carrier status and ask the customer to check the delivery location and household members when appropriate. Open a delivery investigation for orders marked delivered but reported missing. Replacements or refunds require the investigation result and any required approval.",
    "POL-SHIPPING: A package marked delivered but reported missing requires a delivery investigation. Address discrepancies, repeated missing shipment claims, or unusually high order value require the appropriate escalation. No address discrepancy, repeat claim, or high-value concern is documented in this case.",
    "No order number was provided, so the order must be located before any delivery investigation or outcome review can proceed."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Shipping Support"
  ],
  "sources_cited": [
    "KB-205",
    "POL-SHIPPING"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The order cannot be located because no order number was provided and no order date, delivery status, or carrier status is available. Whether the package was marked delivered is unknown, so it is not clear whether a delivery investigation applies. The approved sources do not state who approves a replacement for this case, so the representative should confirm the approval level. The replacement request cannot be assessed until the order and investigation result are available.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about your missing package. I'm sorry for the trouble. To locate your order, please share any of the following: your order number (check your order confirmation email), the name and email address used at checkout, the approximate order date, and the shipping address on the order. Once I can find the order, I can check the carrier status and shipping address. If the order is marked delivered but you have not received it, a delivery investigation may be opened. Replacement requests are reviewed after that investigation is complete, so I can't confirm a replacement at this time.",
  "draft_case_note": "Customer reports a missing package, requests a replacement, and cannot provide an order number. No order date, delivery status, carrier status, or evidence is available. Order lookup details requested in reply. Once the order is located, verify the shipping address and carrier status and check whether it is marked delivered. If so, open a delivery investigation per KB-205 and POL-SHIPPING. No replacement has been approved or promised. Route to Shipping Support. Confidence low due to missing order information."
}
```

## CS-5210 | fields_plus_simulated_message | v3 | severity 15

route=Shipping Support owner=Support Representative policy=Support Representative | approvals=Shipping Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5210",
  "issue_type": "missing_shipment",
  "product_category": "Outdoor clothing",
  "order_number_present": false,
  "missing_information": [
    "Order number (not provided; customer deleted the confirmation email)",
    "Order date (not available)",
    "Delivery status and carrier tracking (not available)",
    "Shipping address on the order for verification",
    "Whether the order was marked delivered by the carrier"
  ],
  "customer_requested_outcome": "Replacement jacket (approximately $112)",
  "key_facts": [
    "Customer states a jacket order never arrived.",
    "No order number is available; customer deleted the confirmation email by accident.",
    "Purchase amount reported as approximately $112 USD.",
    "No evidence provided.",
    "Order lookup has not been completed, so delivery status is unknown."
  ],
  "rule_flags": [
    "KB-205: Orders marked delivered but reported missing require a delivery investigation; replacements or refunds depend on the investigation result and any required approval.",
    "POL-SHIPPING: A package marked delivered but reported missing requires a delivery investigation.",
    "Rule 9: No order number is available, so order lookup details must be requested from the customer and listed as missing information.",
    "Replacement cannot be confirmed until order lookup and delivery investigation are complete."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Shipping Support"
  ],
  "sources_cited": [
    "KB-205",
    "POL-SHIPPING"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "No order number, order date, delivery status, or shipping address is available, so the order cannot yet be identified or verified. Whether the package was delivered or lost is unknown. Any replacement depends on the outcome of a delivery investigation and required approval, which a representative must decide.",
  "draft_reply": "Thank you for reaching out about your jacket order, and I'm sorry it hasn't arrived. To look up your order, could you please share the name on the order, the email address you used to place it, the shipping address it was sent to, and the approximate date you placed it? If you have the last four digits of the payment card used, that can also help us locate it. Once we find the order, we'll check the delivery status with our shipping team and review the options with you. I'm not able to confirm a replacement at this time, but we'll update you once the review is complete.",
  "draft_case_note": "Customer reports jacket order (approx. $112) not received. No order number (confirmation email deleted), no order date, no delivery status, no evidence. Requested replacement. Requested order lookup details (name, email, shipping address, approximate order date, optional payment card last four). No refund or replacement promised. Route to Shipping Support for order lookup and delivery investigation per KB-205 and POL-SHIPPING. Confidence low pending order identification and investigation outcome."
}
```

## CS-5218 | fields_only | v3 | severity 15

route=Shipping Support owner=Support Representative policy=Support Representative | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5218",
  "issue_type": "account_change",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Whether the customer received the delivered package",
    "Reason the customer wants the address changed after delivery",
    "Current order status and delivery address on the order record",
    "Current authorized workflow for post-delivery address changes (not covered in approved sources)"
  ],
  "customer_requested_outcome": "Change the delivery address on an order that has already been delivered.",
  "key_facts": [
    "Phone channel, account issue, order number provided",
    "Order date 2026-10-01; delivery status recorded as Delivered",
    "Purchase amount 95 USD",
    "Customer asks to change address after the order was delivered",
    "No evidence provided"
  ],
  "rule_flags": [
    "Address discrepancy or address-related requests require the appropriate escalation (POL-SHIPPING).",
    "KB-710 is outdated and not authoritative for address changes; the current workflow must be verified by a representative.",
    "Do not state or imply that an address change, refund, replacement, or other action has happened or is approved.",
    "If the customer reports the package was not received, a delivery investigation is required for orders marked delivered but reported missing (POL-SHIPPING, KB-205)."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "POL-SHIPPING",
    "NOTE-KNOWLEDGE-QUALITY",
    "KB-710",
    "KB-205"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The order is marked delivered, and a post-delivery address change falls under an address-related request that policy says needs escalation. KB-710 is outdated and the current address change workflow is not covered in approved sources, so a representative must verify it. Whether the package was received and why the change is requested are unknown.",
  "draft_reply": "Thank you for contacting Alpine Outdoor. I can see your order and its delivery status is marked as delivered. Before any change to your delivery address can be considered, a representative needs to verify the current order status and the workflow that applies to this request, and I'm passing your case to the team that handles shipping and address questions. Could you tell me whether you have received the package, and the reason you need the address changed? Your answers will help the team review your request. I'm not able to confirm that any address change has been made or approved at this time.",
  "draft_case_note": "CS-5218: Customer called requesting an address change on an order marked Delivered (order date 2026-10-01, 95 USD, outdoor clothing). No evidence provided. Order number present. Outdated KB-710 not relied on; current address change workflow must be verified. Address-related request escalated to Shipping Support with Support Lead approval per POL-SHIPPING. Still to confirm: whether customer received the package and reason for change. Customer told a representative is verifying order status and the workflow; no change confirmed or promised. Confidence low."
}
```

## CS-5218 | fields_plus_simulated_message | v3 | severity 15

route=Shipping Support owner=Support Representative policy=Support Representative | approvals=Support Lead (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5218",
  "issue_type": "account_change",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "New shipping address details (not provided in the case)",
    "Current order status verification in the order management system",
    "Carrier delivery confirmation and delivery location for order AO-418218",
    "Whether the customer reports the package as missing or received",
    "Current authorized address-change workflow for orders already marked delivered (KB-710 is outdated and cannot be relied on)"
  ],
  "customer_requested_outcome": "Change the shipping address on order AO-418218 to a new address, even though the order is marked delivered.",
  "key_facts": [
    "Order AO-418218 is provided. Order date is 2026-10-01 and the status is Delivered.",
    "Purchase amount is $95 and the item category is outdoor clothing.",
    "Customer asks to update the shipping address after delivery is recorded.",
    "No evidence was provided with the case.",
    "The customer has not stated that the package is missing."
  ],
  "rule_flags": [
    "POL-SHIPPING: Cases involving an address discrepancy require the appropriate escalation.",
    "NOTE-KNOWLEDGE-QUALITY and KB-710: KB-710 is outdated and not authoritative for address changes. The representative must verify the current workflow before any address-change action.",
    "KB-205: The delivery investigation applies to orders marked delivered but reported missing. The customer has not made that report, so this rule is not triggered by the current facts. Revisit if the customer reports the package missing."
  ],
  "recommended_route": "Shipping Support",
  "required_approvals": [
    "Support Lead"
  ],
  "sources_cited": [
    "POL-SHIPPING",
    "KB-710",
    "NOTE-KNOWLEDGE-QUALITY",
    "KB-205"
  ],
  "confidence": "low",
  "needs_human_judgment_reason": "The order is already marked delivered, the new address is not provided, and the only address-change article (KB-710) is outdated. The current workflow for address changes on delivered orders is not covered in approved sources, so a representative must verify it. The case also involves a possible address discrepancy that requires escalation under POL-SHIPPING. No address change can be confirmed from the available information.",
  "draft_reply": "Thank you for contacting Alpine Outdoor about order AO-418218. I can see that the order is currently marked as delivered. Our team cannot confirm an address change on an order in this status from this conversation. I have passed your request to our shipping team to review the order status and the current address-update process. Could you please share the new address you would like us to note for that review, and let us know whether the package has actually reached you? We will follow up once the review is complete. We cannot guarantee that the address can be changed.",
  "draft_case_note": "CS-5218: Customer requests a shipping address change on order AO-418218 (order date 2026-10-01, status Delivered, $95 outdoor clothing). No new address provided and no evidence attached. KB-710 is outdated and was not used as the workflow source. The current address-change process for delivered orders is not covered in approved sources. Escalated to Shipping Support with Support Lead approval for review under POL-SHIPPING address discrepancy handling. Customer has not reported the package as missing, so KB-205 is not currently triggered. No address change, refund, or other action has been confirmed or promised. Next step: representative to verify current order status and workflow and request the new address details from the customer."
}
```

