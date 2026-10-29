# Alpine Outdoor Customer Support
## Current State Workflow

### Context

Alpine Outdoor sells camping equipment, outdoor clothing, climbing equipment, hiking gear, and related products through its website and retail stores. Customer Support handles inquiries received through chat, email, phone, and store escalation.

### Operational Snapshot

| Measure | Current state |
|---|---:|
| Customer support contacts per month | 6,400 |
| Front line support representatives | 22 |
| Contacts involving returns, exchanges, refunds, shipping, or warranty | 71% |
| Cases requiring one or more follow ups | 37% |
| First contact resolution | 58% |
| Cases escalated for an exception, fraud concern, or high value action | 8% |
| Average resolution time | 15.6 hours |
| Customer satisfaction | 3.9 out of 5 |

### Current Process

| Step | Activity | Primary role | Current challenge |
|---|---|---|---|
| 1 | A customer contacts Alpine Outdoor by chat, email, phone, or store escalation. | Customer; representative | Messages can be vague, emotional, or missing order details. |
| 2 | The representative identifies the order, product, issue, and requested outcome. | Representative | Staff manually extract information and request missing order numbers, photos, or delivery details. |
| 3 | The representative retrieves order, shipping, account, and prior contact information. | Representative | Data is spread across order management, shipping, and support systems. |
| 4 | The representative reviews return, warranty, shipping, exchange, refund, and product guidance. | Representative | Policies vary by product condition, date, value, item type, and reason for contact. |
| 5 | The representative determines the permitted next step and drafts a customer response. | Representative | Similar answers are drafted repeatedly; nuanced cases require careful language. |
| 6 | The representative processes an approved return, exchange, replacement, or refund through controlled systems. | Representative; fulfillment | Actions can affect inventory, payment, customer account, and fraud risk. |
| 7 | The representative escalates exceptions, safety issues, suspected fraud, chargebacks, or high value requests. | Support lead; Fraud; Product Safety; Warranty | Escalations sometimes lack relevant order facts, photos, or prior troubleshooting. |
| 8 | The representative records the outcome and closes the case. | Representative | Resolution notes vary in quality and reduce future search value. |

### Current Bottlenecks

* Representatives read and interpret long or emotionally charged customer messages.
* Missing order numbers, photos, and delivery evidence create follow ups.
* Staff search several policies and product resources to determine allowable actions.
* The distinction between a standard return, defect claim, warranty claim, and exception is not always clear.
* High value refunds and repeated claims need manual review but may be identified late.
* Representatives draft repetitive responses and case notes.

### Control Constraints

* Refunds, replacements, exchanges, account changes, address changes, and payment related actions must use authorized business workflows.
* No system may issue a refund, create a replacement order, override a policy, change account data, or alter shipping details without the required authority.
* Product safety concerns involving climbing, protective, or safety equipment must be escalated to Product Safety.
* Suspected fraud, chargebacks, unusually frequent claims, or bank and payment concerns must be routed to Fraud and Payment Operations.
* Customer information may be used only for the support purpose and through approved systems.

### Improvement Question

Management is considering options to improve issue understanding, policy retrieval, response quality, and routing while preserving appropriate control over business actions. Teams should recommend which work, if any, should be handled by generative AI, deterministic workflows or rules, and humans, with safeguards and measures for any proposed deployment.

### Support Data Note and Data Dictionary

The accompanying file contains a selected sample of 48 support cases. It illustrates routine requests, missing information, policy exceptions, safety concerns, and fraud signals. It is not a statistically representative record of all customer contacts. Use the operational snapshot above, not the sample's category counts, for claims about overall volume or performance.

| Field | Meaning |
|---|---|
| case_id | Unique support case identifier. |
| channel | Original customer contact channel. |
| purchase_channel | Online, retail store, or not applicable when no prior purchase is identified. |
| issue_type | Primary issue assigned after review. |
| product_category | Category of the relevant product. |
| order_number_provided | Whether the customer supplied an order number in the initial contact. |
| order_date | Date of the order when available. |
| delivery_date | Delivery date for eligible online orders when available. |
| case_received_date | Date the support case was received. |
| delivery_status | Current carrier or fulfillment status when available. |
| purchase_amount_usd | Value of the relevant order or item. |
| prior_related_claims_90d | Number of related refund, delivery, or damage claims linked to the account in the prior 90 days. |
| requested_outcome | Primary outcome the customer requested. |
| policy_relevant_facts | Case facts available at initial or latest review. |
| evidence_provided | Supporting evidence such as photos or tracking information. |
| required_next_step | Current control or process step; not an approved final action. |
| assigned_owner | Team or role responsible for the next action. |
| status | Current state at the time of the sample. |
| resolution_hours | Elapsed hours to resolution or current elapsed time. |
| followups | Number of customer or internal follow ups. |
| outcome | Current or final disposition. |
