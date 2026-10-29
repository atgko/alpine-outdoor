# Alpine Outdoor Customer Support
## Policies, Product Knowledge, and Control Rules

### 1. Return, Exchange, and Refund Policy

Standard online purchases may be returned within 30 calendar days of delivery when products are unused, in resalable condition, and include original tags or packaging where applicable. An approved return label may be issued after order verification.

Retail store purchases may be returned to a store within 30 calendar days of purchase when the product is unused, resalable, and accompanied by an acceptable proof of purchase. Store associates use the authorized store return workflow; a return label does not apply.

Exchanges for a different size or color may be offered for eligible unused items, subject to inventory availability. Fulfillment errors may be corrected through the authorized replacement or exchange workflow after order verification.

Used products, products returned outside the standard window, damaged items, and exceptions require review under the applicable policy. A refund must not be issued until the authorized return or refund workflow confirms eligibility and required approval.

### 2. Warranty and Product Safety Policy

Alpine Outdoor's limited warranty covers defects in materials and workmanship under normal intended use. It does not automatically cover ordinary wear, misuse, modification, accident damage, or damage from use outside the product's intended purpose.

Climbing, protective, and safety equipment concerns require Product Safety review when a customer reports a defect, abnormal wear, failure, possible recall, or a potential injury risk. Support staff must not provide safety clearance, inspection advice beyond approved guidance, or a final warranty decision for these items.

### 3. Shipping and Delivery Policy

When a shipment is delayed, representatives may communicate the current carrier status and approved delivery estimate. A package marked delivered but reported missing requires a delivery investigation. Cases involving an address discrepancy, repeated missing shipment claim, or unusually high order value require the appropriate escalation.

### 4. Deterministic Validation and Routing Rules

| Rule | Required outcome |
|---|---|
| Order number is not available | Request order lookup details before account specific action. |
| Standard return is within 30 days and product is unused | Route to the authorized return label workflow after order verification. |
| Retail store return is within 30 days of purchase and proof of purchase is available | Route to the authorized store return workflow. |
| Return is outside 30 days or product condition is unclear | Do not automatically approve. Route for policy review or exception handling. |
| Shipment is marked delivered but reported missing | Open a delivery investigation; do not automatically issue a refund or replacement. |
| Customer reports defect or safety concern involving climbing or protective equipment | Route immediately to Product Safety. |
| Refund or replacement value exceeds $500 | Require Support Lead approval before financial or fulfillment action. |
| Customer has repeated claims, chargeback activity, inconsistent order details, or unusual account behavior | Route to Fraud and Payment Operations. |
| Customer requests an address or account change | Verify identity and use the approved account or order workflow. |

### 5. Authority and AI Governance Requirements

1. Any proposed AI use must rely on approved policy, order, product, and support knowledge sources and must identify or log the basis for its recommendation.
2. Teams proposing AI must define the tasks it performs, data it needs, confidence or uncertainty handling, escalation conditions, and human review points.
3. No AI system may independently issue a refund, create a replacement order, change a shipping address, alter a customer account, approve a warranty claim, override a policy, or close a fraud or safety concern.
4. AI generated customer communication must be governed by the team's proposed risk based design and must not claim that a financial or fulfillment action has occurred unless the authorized system confirms it.
5. Customer data must remain in approved systems and be used only for the support purpose.
6. The organization must be able to audit recommendations, retrieved sources, human edits, actions taken, escalations, and reported errors.

### 6. Selected Product and Knowledge Resource Excerpts

#### KB 101: Standard Return Label

Last reviewed: September 15, 2026. Owner: Customer Experience.

After order verification, a return label may be issued for an online purchase within 30 calendar days of delivery when the item is unused and resalable. Do not issue a label for items requiring Product Safety, Fraud, Warranty, or Support Lead review until that review is complete.

#### KB 205: Missing Package Marked Delivered

Last reviewed: September 20, 2026. Owner: Shipping Operations.

Confirm the shipping address and carrier status. Ask the customer to check the delivery location and household members when appropriate. Open a delivery investigation for orders marked delivered but reported missing. Replacements or refunds require the result of the investigation and any required approval.

#### KB 318: Limited Warranty Assessment

Last reviewed: August 30, 2026. Owner: Warranty.

Collect the order number, product, purchase date, description of the concern, and photos or video when available. Warranty staff determine whether the concern is covered. For climbing and safety equipment, forward the case to Product Safety before describing a final remedy.

#### KB 427: Climbing Equipment Safety Concern

Last reviewed: October 3, 2026. Owner: Product Safety.

Any report of a defective carabiner, harness, rope, helmet, belay device, or protective equipment should be recorded and routed to Product Safety. Do not instruct the customer to continue using the product. Do not advise on repair or inspection beyond approved recall or return instructions.

#### KB 510: Product Care for Waterproof Clothing

Last reviewed: July 18, 2026. Owner: Product.

Care requirements vary by garment. Refer customers to the specific product care page when available. Do not state that an item remains eligible for return after washing or tag removal; return eligibility depends on the policy and product condition.

#### KB 612: Camp Stove Safety

Last reviewed: October 5, 2026. Owner: Product Safety.

Portable camp stoves are for outdoor use in well ventilated areas only. They must not be used indoors, in tents, in vehicles, or in other enclosed spaces. The support team may provide this safety guidance and direct customers to the product manual.

#### KB 710: Remote Address Change Process

Last reviewed: February 1, 2025. Owner: Order Operations.

Customers can update their delivery address through their account before an order is processed. This article is under review because the order management system changed in September 2026. Representatives should verify the current order status and use the current authorized workflow rather than relying on this article alone.

### 7. Knowledge Quality Notes

* KB 710 is outdated and must not be treated as an authoritative source for address changes.
* Product Safety maintains recall notices separately from the general knowledge base. Recall status requires the product identifier or serial range when applicable.
* The support knowledge base does not currently provide a standard explanation for customers whose return is denied because the product was used.
* Fraud and Payment Operations does not publish its detailed detection criteria to front line representatives.

### 8. Measures for an Improvement Pilot

Compare baseline and pilot results by issue type, channel, product category, order value, and escalation category. Possible measures include first response time, resolution time, first contact resolution, correct routing rate, policy accuracy, customer satisfaction, reopen rate, human review rate, refund error rate, fraud loss, safety escalation timeliness, representative handling time, and source coverage.

An improvement should not be judged successful solely by reducing handling time. It must preserve accurate policy application, customer trust, financial control, fraud detection, and product safety.
