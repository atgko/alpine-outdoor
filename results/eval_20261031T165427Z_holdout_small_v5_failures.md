# Worst records for manual review

Ordered by a simple severity score (see eval/metrics.py). Top 10 of 3 records with any failure.

## CS-5237 | fields_only | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5237",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Model or variant of the item ordered, to compare against the item received",
    "Model or variant of the item received, as confirmed by the customer or the photo",
    "Current condition of the received item, including whether it is unused and whether original tags or packaging are present",
    "Whether the customer has already removed tags or worn or washed the item"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Order number was provided. Order date is 2026-10-07.",
    "Order status is Delivered.",
    "Customer reports receiving a different model than ordered.",
    "Customer attached a photo.",
    "Purchase amount is $160 USD.",
    "Contact channel is Phone.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Rule R8 could not be evaluated because the prior related claims count in the last 90 days is unknown."
  ],
  "rule_flags": ["T1"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN"],
  "confidence": "low",
  "needs_human_judgment_reason": "The rule layer routes this case to Fulfillment Support because of a possible fulfillment error (T1). The customer's photo and the ordered model are not yet compared in the case, so the wrong-item claim is unverified. Item condition is unknown: POL-RETURN allows exchange or fulfillment-error correction only after order verification, and a refund may not be issued until the authorized return or refund workflow confirms eligibility and required approval. Rule R8 could not be evaluated because the prior related claims count is unknown, so the internal check is incomplete. The representative should confirm the ordered and received models, verify the order, and determine whether the fulfillment error workflow applies, which may offer a replacement or exchange rather than a refund. Policy coverage for refunds on fulfillment errors beyond these steps is not covered in approved sources.",
  "draft_reply": "Thank you for calling Alpine Outdoor and for sending the photo of the item you received. We have noted that the item received on your order does not match the model you ordered. Your case has been referred to our Fulfillment Support team, who will review your order and the photo. We are not able to confirm a refund at this time. Once the review is complete, a representative will contact you about the next steps available for your order. To help with the review, please keep the item and its tags or packaging, if you still have them, and let us know the model name or style number printed on the item you received.",
  "draft_case_note": "CS-5237: Customer reports receiving a different model than ordered on a delivered outdoor clothing order ($160). Customer requests refund and provided a photo. Rule T1 fired (possible fulfillment error), routed to Fulfillment Support. Rule R8 not evaluable (prior related claims count unknown). Item condition and ordered vs. received models not yet verified. No refund or replacement promised. Customer told the case is under Fulfillment Support review and asked to keep the item and provide the model or style number. Representative to verify the order and determine the applicable fulfillment error path under POL-RETURN. Confidence low."
}
```

## CS-5237 | fields_plus_simulated_message | v5 | severity 15

route=Fulfillment Support owner=Support Representative policy=Support Representative | approvals=Fulfillment Support (expected -) | violations=- | warnings=- | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5237",
  "issue_type": "wrong_item",
  "product_category": "Outdoor clothing",
  "order_number_present": true,
  "missing_information": [
    "Model name or SKU of the jacket ordered and of the jacket received, to confirm the mismatch",
    "Condition of the received jacket, including whether it is unused and whether original tags or packaging are present",
    "Customer's preferred resolution if an exchange or replacement is offered instead of a refund",
    "Internal check for prior related claims in the last 90 days could not be completed because the information is unavailable"
  ],
  "customer_requested_outcome": "Refund",
  "key_facts": [
    "Customer reports receiving a different jacket model than the one ordered (order AO-418237).",
    "Customer provided a photo.",
    "Order date 2026-10-07; delivery status: Delivered.",
    "Purchase amount: 160 USD.",
    "Channel: Phone.",
    "Rule T1 fired: possible fulfillment error, routed to Fulfillment Support.",
    "Policy POL-RETURN states fulfillment errors may be corrected through the authorized replacement or exchange workflow after order verification, and a refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval.",
    "Rule R8 could not be evaluated due to missing information."
  ],
  "rule_flags": ["T1", "R8"],
  "recommended_route": "Fulfillment Support",
  "required_approvals": ["Fulfillment Support"],
  "sources_cited": ["POL-RETURN"],
  "confidence": "low",
  "needs_human_judgment_reason": "The customer reports a wrong jacket model, which the rule layer routes to Fulfillment Support as a possible fulfillment error. The approved policy says fulfillment errors go through the authorized replacement or exchange workflow after order verification, and a refund requires confirmation from the authorized return or refund workflow. The customer asked for a refund, but the sources do not establish which resolution applies. Item condition, tags, and the specific models ordered and received are not confirmed. Rule R8 could not be evaluated because required information is unavailable, so the representative should resolve that check before any outcome is decided. Sources do not cover how a refund versus exchange is chosen for a wrong-item case.",
  "draft_reply": "Thank you for calling Alpine Outdoor about order AO-418237, and for sending the photo of the jacket you received. I'm sorry the item you received isn't the one you ordered. I've noted your concern and referred your case to our Fulfillment Support team to review the order and the item received. Please note this is a review and not a confirmation of a refund or any other outcome; the team will determine the next step once the review is complete. To help with the review, could you tell me the model name or product code printed on the jacket you received, and whether it has its original tags or packaging and has been worn or washed? We will follow up with you once the review is complete.",
  "draft_case_note": "CS-5237 (Phone). Customer reports receiving a different jacket model than ordered on order AO-418237 (order date 2026-10-07, delivered, 160 USD). Photo attached. Customer requests refund. Rule T1 fired (possible fulfillment error), routed to Fulfillment Support. Rule R8 could not be evaluated due to missing information. Per POL-RETURN, fulfillment errors go through the authorized replacement or exchange workflow after order verification; refund requires confirmation from the authorized return or refund workflow. No refund or other outcome promised. Missing: ordered vs received model/SKU, item condition and tags, customer's preferred resolution. Draft reply sent for representative review; representative to request model and condition details and route to Fulfillment Support."
}
```

## CS-5202 | fields_plus_simulated_message | v5 | severity 1

route=Support Representative owner=Support Representative policy=Support Representative | approvals=- (expected -) | violations=- | warnings=stop_use_advice | api_ok=True schema_valid=True

```
{
  "case_id": "CS-5202",
  "issue_type": "damaged",
  "product_category": "Camping equipment",
  "order_number_present": true,
  "missing_information": [
    "Whether the damage occurred in shipping or was a fulfillment error (not covered in approved sources)",
    "Prior related claims in the last 90 days (needed to evaluate rule R8)",
    "Product identifier or serial information for the tent, if the review requires it (not covered in approved sources)"
  ],
  "customer_requested_outcome": "Replacement of the tent after a pole arrived bent",
  "key_facts": [
    "Order AO-418202, order date 2026-10-02, status Delivered, purchase amount $245 USD",
    "Customer reports one tent pole arrived bent",
    "Customer states the purchase was less than a month ago",
    "Customer attached photos of the damage",
    "Channel: Chat",
    "Rule layer: no rules fired; default route is Support Representative; no required approvals",
    "R8 could not be evaluated because prior_related_claims_90d is unknown"
  ],
  "rule_flags": [],
  "recommended_route": "Support Representative",
  "required_approvals": [],
  "sources_cited": ["POL-RETURN"],
  "confidence": "low",
  "needs_human_judgment_reason": "Item condition and the damage claim need representative review. POL-RETURN states that damaged items require review under the applicable policy and that a refund must not be issued until the authorized workflow confirms eligibility. The approved sources do not state how a damaged replacement is handled for a delivered item, or whether the damage is a shipping issue or a fulfillment error. The rule layer could not evaluate R8 because prior related claims in the last 90 days are unknown, so the representative should confirm that before any decision. The sources do not provide guidance on whether a bent tent pole is safe to use, so no safety or repair advice is given.",
  "draft_reply": "Thank you for reaching out about order AO-418202, and for sending photos of the bent tent pole. I'm sorry the tent arrived damaged. I've noted your request for a replacement. A representative will review the damage claim and the order details, and they will contact you with the outcome. I can't confirm a replacement at this time. Please don't use the tent in the meantime, because we can't offer guidance on whether the damaged pole is safe to use. Is there anything else about the delivery that would help us with the review?",
  "draft_case_note": "CS-5202, Chat. Customer reports tent pole arrived bent on order AO-418202 (order date 2026-10-02, delivered, $245). Photos attached. Customer requests replacement. Rule layer: no rules fired; route Support Representative; no approvals required. R8 not evaluated because prior_related_claims_90d is unknown. Missing: cause of damage (shipping vs fulfillment), prior claims count. Replacement not confirmed or promised; damage claim referred for representative review under POL-RETURN. Customer told not to use item pending review. Confidence low due to item condition review and missing R8 facts."
}
```

