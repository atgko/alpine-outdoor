"""Structured output schema (prompt versions v2 to v4) and validation."""
from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

IssueType = Literal[
    "return", "exchange", "refund", "damaged", "wrong_item", "missing_shipment",
    "shipping_delay", "warranty", "product_safety", "chargeback", "fraud_signal",
    "account_change", "product_question", "other",
]
Route = Literal[
    "Support Representative", "Support Lead", "Warranty Team", "Product Safety",
    "Fraud and Payment Operations", "Shipping Support", "Fulfillment Support",
]
ROUTES: tuple[str, ...] = Route.__args__


class TriageOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    issue_type: IssueType
    product_category: str
    order_number_present: bool
    missing_information: list[str]
    customer_requested_outcome: str
    key_facts: list[str]
    rule_flags: list[str]
    recommended_route: Route
    required_approvals: list[Route]
    sources_cited: list[str]
    confidence: Literal["high", "medium", "low"]
    needs_human_judgment_reason: str
    draft_reply: str
    draft_case_note: str


# The JSON template shown to the model in v2 to v4 prompts.
SCHEMA_TEMPLATE = """{
  "case_id": "",
  "issue_type": "return | exchange | refund | damaged | wrong_item | missing_shipment | shipping_delay | warranty | product_safety | chargeback | fraud_signal | account_change | product_question | other",
  "product_category": "",
  "order_number_present": true,
  "missing_information": [],
  "customer_requested_outcome": "",
  "key_facts": [],
  "rule_flags": [],
  "recommended_route": "Support Representative | Support Lead | Warranty Team | Product Safety | Fraud and Payment Operations | Shipping Support | Fulfillment Support",
  "required_approvals": [],
  "sources_cited": [],
  "confidence": "high | medium | low",
  "needs_human_judgment_reason": "",
  "draft_reply": "",
  "draft_case_note": ""
}"""


def extract_json(text: str) -> str | None:
    """Return the outermost {...} block, ignoring code fences or prose around it."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE)
    start, end = text.find("{"), text.rfind("}")
    return text[start:end + 1] if 0 <= start < end else None


def parse_output(text: str) -> tuple[TriageOutput | None, str | None]:
    """Validate model text. Returns (output, None) or (None, error message)."""
    raw = extract_json(text or "")
    if raw is None:
        return None, "no JSON object found"
    try:
        return TriageOutput.model_validate(json.loads(raw)), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"
    except ValidationError as exc:
        return None, f"schema validation failed: {exc.error_count()} errors: {exc.errors()[0]['loc']}"
