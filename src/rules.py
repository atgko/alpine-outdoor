"""Deterministic rule layer.

Rules return flags and a required route. They never return or perform an
action. The model cannot override this layer.

Each rule evaluates to one of three states:
  fired            the known facts prove the rule applies
  not_fired        the known facts prove it does not apply
  cannot_evaluate  a needed fact is unknown, so the rule does not guess

Rule origins:
  client          the nine rules in section 4 of the client policy file
  team_proposed   TEAM PROPOSED additions (T1, T2), not client rules
  policy_derived  W1: warranty claims go to the Warranty Team. Comes from
                  policy section 2 and KB 318, not from the section 4 table.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from src.case_facts import CaseFacts

FIRED, NOT_FIRED, CANNOT_EVALUATE = "fired", "not_fired", "cannot_evaluate"
CLIENT, TEAM_PROPOSED, POLICY_DERIVED = "client", "team_proposed", "policy_derived"

FRAUD = "Fraud and Payment Operations"
SAFETY = "Product Safety"
WARRANTY = "Warranty Team"
LEAD = "Support Lead"
SHIPPING = "Shipping Support"
FULFILLMENT = "Fulfillment Support"
REP = "Support Representative"

# TEAM DECISION (made after seeing the sample cases, not defined by the
# client): when several rules fire, the highest route in this list becomes
# primary_route. Shipping and Fulfillment Support share a level; Shipping is
# listed first only to make the order deterministic.
ROUTE_PRIORITY = (FRAUD, SAFETY, WARRANTY, LEAD, SHIPPING, FULFILLMENT, REP)
DEFAULT_ROUTE = REP

RETURN_TYPES = {"return", "exchange"}
FINANCIAL_OUTCOMES = {"Refund", "Replacement", "Repair or replacement"}
HIGH_VALUE_USD = 500
REPEATED_CLAIMS_MIN = 2  # client does not define "repeated"; see QUESTIONS.md
STALLED_DAYS = 7
NOT_YET_SHIPPED = {"Label created", "Processing"}


# Three-valued logic helpers. None means unknown.
def _not(x: bool | None) -> bool | None:
    return None if x is None else not x


def _all(*xs: bool | None) -> bool | None:
    if any(x is False for x in xs):
        return False
    return None if any(x is None for x in xs) else True


def _any(*xs: bool | None) -> bool | None:
    if any(x is True for x in xs):
        return True
    return None if any(x is None for x in xs) else False


def _eq(x, value) -> bool | None:
    return None if x is None else x == value


def _in(x, values) -> bool | None:
    return None if x is None else x in values


def _gt(x, limit) -> bool | None:
    return None if x is None else x > limit


def _ge(x, limit) -> bool | None:
    return None if x is None else x >= limit


def _is_return(f: CaseFacts) -> bool | None:
    return _in(f.issue_type, RETURN_TYPES)


def _stalled_shipment_route(f: CaseFacts) -> str:
    # TEAM DECISION: not yet shipped -> Fulfillment, otherwise Shipping.
    return FULFILLMENT if f.delivery_status in NOT_YET_SHIPPED else SHIPPING


@dataclass(frozen=True)
class Rule:
    id: str
    origin: str
    rule_text: str
    inputs: tuple[str, ...]
    test: Callable[[CaseFacts], bool | None]
    reason: str
    route: str | Callable[[CaseFacts], str]


@dataclass(frozen=True)
class Flag:
    rule_id: str
    status: str
    reason: str
    rule_text: str
    origin: str
    route: str | None  # set only when the rule fired
    unknown_inputs: tuple[str, ...]


@dataclass(frozen=True)
class RuleResult:
    case_id: str
    flags: tuple[Flag, ...]
    primary_route: str
    required_approvals: tuple[str, ...]
    default_route_used: bool

    @property
    def fired(self) -> tuple[Flag, ...]:
        return tuple(f for f in self.flags if f.status == FIRED)

    @property
    def cannot_evaluate(self) -> tuple[Flag, ...]:
        return tuple(f for f in self.flags if f.status == CANNOT_EVALUATE)


RULES = (
    Rule(
        "R1", CLIENT,
        "Order number is not available | Request order lookup details before account specific action.",
        ("order_number_present",),
        lambda f: _not(f.order_number_present),
        "No order number provided. Request order lookup details before any account specific step.",
        REP,
    ),
    Rule(
        "R2", CLIENT,
        "Standard return is within 30 days and product is unused | Route to the authorized return label workflow after order verification.",
        ("issue_type", "purchase_channel", "within_30_days", "item_unused"),
        lambda f: _all(_is_return(f), _eq(f.purchase_channel, "online"), f.within_30_days, f.item_unused),
        "Online return within 30 days and unused. Route to the authorized return label workflow after order verification.",
        REP,
    ),
    Rule(
        "R3", CLIENT,
        "Retail store return is within 30 days of purchase and proof of purchase is available | Route to the authorized store return workflow.",
        ("issue_type", "purchase_channel", "within_30_days", "proof_of_purchase"),
        lambda f: _all(_is_return(f), _eq(f.purchase_channel, "store"), f.within_30_days, f.proof_of_purchase),
        "Store return within 30 days with proof of purchase. Route to the authorized store return workflow.",
        REP,
    ),
    Rule(
        "R4", CLIENT,
        "Return is outside 30 days or product condition is unclear | Do not automatically approve. Route for policy review or exception handling.",
        ("issue_type", "within_30_days", "item_unused"),
        # item_unused False (used) or None (condition unclear) both count.
        lambda f: _all(_is_return(f), _any(_not(f.within_30_days), _not(f.item_unused), f.item_unused is None)),
        "Return is outside 30 days, or the item is used or its condition is unclear. No automatic approval; policy review.",
        LEAD,  # TEAM DECISION: client does not name the review owner.
    ),
    Rule(
        "R5", CLIENT,
        "Shipment is marked delivered but reported missing | Open a delivery investigation; do not automatically issue a refund or replacement.",
        ("issue_type", "delivery_status"),
        lambda f: _all(_eq(f.issue_type, "missing_shipment"), _eq(f.delivery_status, "Delivered")),
        "Marked delivered but reported missing. Open a delivery investigation; no automatic refund or replacement.",
        SHIPPING,  # TEAM DECISION: client does not name the owner.
    ),
    Rule(
        "R6", CLIENT,
        "Customer reports defect or safety concern involving climbing or protective equipment | Route immediately to Product Safety.",
        ("protective_item", "defect_or_safety_reported"),
        lambda f: _all(f.protective_item, f.defect_or_safety_reported),
        "Defect or safety concern on climbing or protective equipment. Route immediately to Product Safety.",
        SAFETY,
    ),
    Rule(
        "R7", CLIENT,
        "Refund or replacement value exceeds $500 | Require Support Lead approval before financial or fulfillment action.",
        ("amount_usd", "requested_outcome"),
        lambda f: _all(_gt(f.amount_usd, HIGH_VALUE_USD), _in(f.requested_outcome, FINANCIAL_OUTCOMES)),
        "Refund or replacement value over $500. Support Lead approval required before any financial or fulfillment action.",
        LEAD,
    ),
    Rule(
        "R8", CLIENT,
        "Customer has repeated claims, chargeback activity, inconsistent order details, or unusual account behavior | Route to Fraud and Payment Operations.",
        ("issue_type", "fraud_signal_in_text", "prior_related_claims_90d"),
        lambda f: _any(
            _in(f.issue_type, {"chargeback", "fraud_signal"}),
            f.fraud_signal_in_text,
            _ge(f.prior_related_claims_90d, REPEATED_CLAIMS_MIN),
        ),
        "Repeated claims, chargeback, or unusual account activity. Route to Fraud and Payment Operations.",
        FRAUD,
    ),
    Rule(
        "R9", CLIENT,
        "Customer requests an address or account change | Verify identity and use the approved account or order workflow.",
        ("address_or_account_change",),
        lambda f: f.address_or_account_change,
        "Address or account change requested. Verify identity and use the approved account or order workflow.",
        REP,
    ),
    Rule(
        "W1", POLICY_DERIVED,
        "Policy section 2 and KB 318: Warranty staff determine whether the concern is covered.",
        ("issue_type",),
        lambda f: _eq(f.issue_type, "warranty"),
        "Warranty claim. Warranty staff determine coverage.",
        WARRANTY,
    ),
    Rule(
        "T1", TEAM_PROPOSED,
        "TEAM PROPOSED: Fulfillment error (wrong item, wrong color, duplicate or wrong pair) | Route to Fulfillment Support.",
        ("fulfillment_error_reported",),
        lambda f: f.fulfillment_error_reported,
        "Possible fulfillment error. Route to Fulfillment Support.",
        FULFILLMENT,
    ),
    Rule(
        "T2", TEAM_PROPOSED,
        "TEAM PROPOSED: Shipment not moving for 7 or more days and not marked delivered | Route to Shipping Support or Fulfillment Support.",
        ("issue_type", "delivery_status", "days_without_movement"),
        lambda f: _all(
            _in(f.issue_type, {"missing_shipment", "shipping_delay"}),
            _not(_eq(f.delivery_status, "Delivered")),
            _ge(f.days_without_movement, STALLED_DAYS),
        ),
        "Shipment has not moved for 7 or more days and is not marked delivered.",
        _stalled_shipment_route,
    ),
)

CLIENT_RULE_IDS = frozenset(r.id for r in RULES if r.origin == CLIENT)
ALL_RULE_IDS = frozenset(r.id for r in RULES)


def _evaluate_rule(rule: Rule, facts: CaseFacts) -> Flag:
    value = rule.test(facts)
    unknown = tuple(name for name in rule.inputs if getattr(facts, name) is None)
    if value is True:
        route = rule.route(facts) if callable(rule.route) else rule.route
        return Flag(rule.id, FIRED, rule.reason, rule.rule_text, rule.origin, route, unknown)
    if value is None:
        reason = "Cannot evaluate: unknown " + ", ".join(unknown)
        return Flag(rule.id, CANNOT_EVALUATE, reason, rule.rule_text, rule.origin, None, unknown)
    return Flag(rule.id, NOT_FIRED, "Conditions not met.", rule.rule_text, rule.origin, None, unknown)


def evaluate(facts: CaseFacts, enabled: frozenset[str] = ALL_RULE_IDS) -> RuleResult:
    """Run every enabled rule and pick a route. Never returns an action."""
    flags = tuple(_evaluate_rule(r, facts) for r in RULES if r.id in enabled)
    routes = {f.route for f in flags if f.status == FIRED}
    ordered = tuple(r for r in ROUTE_PRIORITY if r in routes)
    return RuleResult(
        case_id=facts.case_id,
        flags=flags,
        primary_route=ordered[0] if ordered else DEFAULT_ROUTE,
        required_approvals=tuple(r for r in ordered if r != DEFAULT_ROUTE),
        default_route_used=not ordered,
    )
