"""Case facts used by the rule layer.

Every fact can be None, which means "unknown". The rule layer never guesses
an unknown fact. Each fact is tagged with where it came from:

  structured  a CSV field
  extracted   read from free text (keywords here; the LLM in Stage 2)
  inferred    derived from another field, with the assumption documented

`from_csv_row` is the Stage 1 keyword reader. It reads only the
`policy_relevant_facts` summary; the CSV has no raw customer message.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

STRUCTURED = "structured"
EXTRACTED = "extracted"
INFERRED = "inferred"

# CSV issue_type -> schema issue_type. Documented in README.
ISSUE_TYPE_MAP = {
    "Return": "return",
    "Exchange": "exchange",
    "Refund request": "refund",
    "Damaged product": "damaged",
    "Incorrect order": "wrong_item",
    "Wrong item": "wrong_item",
    "Missing shipment": "missing_shipment",
    "Shipping delay": "shipping_delay",
    "Warranty claim": "warranty",
    "Product safety concern": "product_safety",
    "Chargeback": "chargeback",
    "Duplicate claim": "fraud_signal",
    "Potential fraud": "fraud_signal",
    "Account issue": "account_change",
    "Product question": "product_question",
}

PROTECTIVE_KEYWORDS = r"carabiner|harness|\brope\b|helmet|belay|protective"
DEFECT_KEYWORDS = (
    r"defect|damag|does not close|fail|\bwear\b|abrasion|broken|crack|torn|"
    r"\btear\b|frayed|bent|recall|safety|leak"
)
DEFECT_ISSUE_TYPES = {"damaged", "warranty", "product_safety"}
FRAUD_KEYWORDS = (
    r"chargeback|disputes? (?:the |a )?(?:card )?charge|"
    r"\b(?:second|third|fourth|fifth) \w+ claim|repeated claims?|"
    r"multiple .*refund requests|changing (?:delivery )?addresses"
)
# Keywords from the TEAM PROPOSED fulfillment-error rule text:
# wrong item, wrong color, duplicate, wrong pair.
FULFILLMENT_KEYWORDS = (
    r"wrong (?:\w+ )?(?:item|colou?r|pair)|\bduplicate\b|\binstead of\b|"
    r"\btwo (?:left|right)\b|different model"
)
UNUSED_KEYWORDS = r"\bunused\b|\bunopened\b|tags attached"
USED_KEYWORDS = r"\bused\b|\bworn\b|washed|tags removed"


@dataclass(frozen=True)
class CaseFacts:
    case_id: str
    issue_type: str | None = None
    product_category: str | None = None
    order_number_present: bool | None = None
    amount_usd: float | None = None
    requested_outcome: str | None = None
    delivery_status: str | None = None
    purchase_channel: str | None = None  # "online" or "store"
    within_30_days: bool | None = None
    item_unused: bool | None = None  # False = used, None = condition unclear
    proof_of_purchase: bool | None = None
    protective_item: bool | None = None  # climbing or protective equipment
    defect_or_safety_reported: bool | None = None
    fraud_signal_in_text: bool | None = None
    prior_related_claims_90d: int | None = None  # not in the CSV
    fulfillment_error_reported: bool | None = None
    days_without_movement: int | None = None
    address_or_account_change: bool | None = None
    sources: dict[str, str] = field(default_factory=dict)


def _has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE) is not None


def read_within_30_days(text: str) -> bool | None:
    if _has(r"within 30 days", text):
        return True
    if _has(r"outside (?:the )?(?:return )?window", text):
        return False
    m = re.search(r"(\d+) days (?:after delivery|old)", text, re.IGNORECASE)
    return int(m.group(1)) <= 30 if m else None


def read_item_unused(text: str) -> bool | None:
    unused, used = _has(UNUSED_KEYWORDS, text), _has(USED_KEYWORDS, text)
    if unused == used:  # neither mentioned, or both: condition unclear
        return None
    return unused


def read_days_without_movement(text: str) -> int | None:
    m = re.search(r"(?:not moved|no movement)\D{0,20}?(\d+)\s+days", text, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _blank_to_none(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


def from_csv_row(row: dict[str, str]) -> CaseFacts:
    """Build CaseFacts from one CSV row: structured fields plus keyword reading."""
    text = row.get("policy_relevant_facts", "")
    issue_type = ISSUE_TYPE_MAP.get(row["issue_type"], "other")
    category = _blank_to_none(row.get("product_category"))
    status = _blank_to_none(row.get("delivery_status"))
    outcome = _blank_to_none(row.get("requested_outcome"))
    amount = _blank_to_none(row.get("purchase_amount_usd"))
    is_climbing = category == "Climbing equipment"

    sources = {
        "issue_type": STRUCTURED,
        "product_category": STRUCTURED,
        "order_number_present": STRUCTURED,
        "amount_usd": STRUCTURED,
        "requested_outcome": STRUCTURED,
        "delivery_status": STRUCTURED,
        # Only online orders ship, so a delivery status implies online.
        "purchase_channel": INFERRED,
        "within_30_days": EXTRACTED,
        "item_unused": EXTRACTED,
        "protective_item": STRUCTURED if is_climbing else EXTRACTED,
        "defect_or_safety_reported": EXTRACTED,
        "fraud_signal_in_text": EXTRACTED,
        "fulfillment_error_reported": EXTRACTED,
        "days_without_movement": EXTRACTED,
        "address_or_account_change": STRUCTURED,
    }
    return CaseFacts(
        case_id=row["case_id"],
        issue_type=issue_type,
        product_category=category,
        order_number_present={"Yes": True, "No": False}.get(row.get("order_number_provided", "")),
        amount_usd=float(amount) if amount else None,
        requested_outcome=outcome,
        delivery_status=status,
        purchase_channel="online" if status else None,
        within_30_days=read_within_30_days(text),
        item_unused=read_item_unused(text),
        protective_item=is_climbing or _has(PROTECTIVE_KEYWORDS, text),
        defect_or_safety_reported=issue_type in DEFECT_ISSUE_TYPES or _has(DEFECT_KEYWORDS, text),
        fraud_signal_in_text=_has(FRAUD_KEYWORDS, text),
        fulfillment_error_reported=issue_type == "wrong_item" or _has(FULFILLMENT_KEYWORDS, text),
        days_without_movement=read_days_without_movement(text),
        address_or_account_change=issue_type == "account_change" or "address" in (outcome or "").lower(),
        sources=sources,
    )
