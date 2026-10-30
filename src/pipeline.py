"""Run one case end to end for one prompt version and return a log record.

Steps: build the prompt (case, plus sources from v3, plus rule flags from v4),
call the model, validate JSON (v2 onwards, one retry on invalid output), apply
the rule layer override (v4 and v5), run guardrail checks on the customer
facing text, and return everything needed for the JSONL run log.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.case_facts import ISSUE_TYPE_MAP, from_csv_row
from src.guardrails import check_draft, check_sources
from src.kb import load_kb, select_sources
from src.rules import FIRED, RuleResult, evaluate
from src.schema import ROUTES, SCHEMA_TEMPLATE, parse_output

PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
VERSIONS = ("v1", "v2", "v3", "v4", "v5")
GROUNDED = {"v3", "v4", "v5"}  # approved sources in the prompt
HYBRID = {"v4", "v5"}  # rule layer results in the prompt, plus the route override
FIELDS_ONLY, WITH_MESSAGE = "fields_only", "fields_plus_simulated_message"

# Only these CSV fields are shown to the model. required_next_step,
# assigned_owner, status, resolution_hours, followups and outcome are labels
# or later process data and must never be in the prompt.
INPUT_FIELDS = (
    "case_id", "channel", "issue_type", "product_category", "order_number_provided",
    "order_date", "delivery_status", "purchase_amount_usd", "requested_outcome",
    "policy_relevant_facts", "evidence_provided",
)
KB = load_kb()


@dataclass(frozen=True)
class Prompt:
    version: str
    system: str
    user: str
    sha256: str


def load_prompt(version: str) -> Prompt:
    text = (PROMPT_DIR / f"{version}.md").read_text(encoding="utf-8")
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    system = body.split("## SYSTEM", 1)[1].split("## USER", 1)[0].strip()
    user = body.split("## USER", 1)[1].strip()
    return Prompt(version, system, user, hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])


def render_case(row: dict[str, str], message: str | None) -> str:
    lines = [f"{name}: {row.get(name) or 'not available'}" for name in INPUT_FIELDS]
    text = "<case_fields>\n" + "\n".join(lines) + "\n</case_fields>"
    if message is not None:
        text += f"\n\n<customer_message simulated=\"true\">\n{message}\n</customer_message>"
    return text


def render_sources(ids: tuple[str, ...]) -> str:
    blocks = []
    for sid in ids:
        s = KB[sid]
        status = "yes" if s.authoritative else "NO (outdated, verify the current workflow)"
        blocks.append(f"[{s.id}] {s.title}\nOwner: {s.owner}. Last reviewed: {s.last_reviewed}. "
                      f"Authoritative: {status}\n{s.body}")
    return "\n\n".join(blocks)


def render_rules(result: RuleResult) -> str:
    fired = [f"- {f.rule_id} ({f.origin}): {f.reason} Route: {f.route}" for f in result.fired]
    unknown = [f"- {f.rule_id}: {f.reason}" for f in result.cannot_evaluate]
    return "\n".join([
        "Rules fired:", *(fired or ["- none (default route: Support Representative)"]),
        "Rules that could not be evaluated (facts missing, do not guess):", *(unknown or ["- none"]),
        f"Primary route from rule layer: {result.primary_route}",
        f"Required approvals from rule layer: {', '.join(result.required_approvals) or 'none'}",
    ])


def route_from_text(text: str) -> str | None:
    """v1 has no schema: take the first route name mentioned in the reply."""
    found = [(m.start(), r) for r in ROUTES if (m := re.search(re.escape(r), text, re.I))]
    return min(found)[1] if found else None


def build_inputs(version: str, row: dict[str, str], message: str | None):
    prompt = load_prompt(version)
    facts = from_csv_row(row)
    rule_result = evaluate(facts) if version in HYBRID else None
    issue_type = ISSUE_TYPE_MAP.get(row["issue_type"], "other")
    sources = select_sources(issue_type, f"{row['policy_relevant_facts']} {message or ''}") \
        if version in GROUNDED else ()
    user = (prompt.user.replace("{{case}}", render_case(row, message))
            .replace("{{schema}}", SCHEMA_TEMPLATE)
            .replace("{{sources}}", render_sources(sources))
            .replace("{{rules}}", render_rules(rule_result) if rule_result else ""))
    return prompt, user, sources, rule_result


def run_case(row: dict[str, str], version: str, client, split: str,
             message: str | None = None, injection_present: bool = False) -> dict:
    prompt, user, sources, rule_result = build_inputs(version, row, message)
    calls = [client.call(prompt.system, user)]
    parsed, schema_error = None, None
    if version != "v1" and calls[-1].ok:
        parsed, schema_error = parse_output(calls[-1].text)
        if parsed is None:  # one retry on invalid output, then a logged failure
            calls.append(client.call(prompt.system, user))
            if calls[-1].ok:
                parsed, schema_error = parse_output(calls[-1].text)
    last = calls[-1]

    model_route = parsed.recommended_route if parsed else (route_from_text(last.text) if version == "v1" else None)
    final_route, approvals, disagreed = model_route, list(parsed.required_approvals) if parsed else [], None
    if rule_result is not None and rule_result.fired:
        final_route = rule_result.primary_route
        approvals = list(dict.fromkeys([*rule_result.required_approvals, *approvals]))
        disagreed = None if model_route is None else model_route != rule_result.primary_route

    draft = parsed.draft_reply if parsed else last.text
    note = parsed.draft_case_note if parsed else ""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "prompt_version": version, "prompt_hash": prompt.sha256,
        "provider": last.provider, "model": last.model,
        "case_id": row["case_id"], "split": split,
        "mode": WITH_MESSAGE if message is not None else FIELDS_ONLY,
        "input": {"system": prompt.system, "user": user},
        "raw_outputs": [c.text for c in calls],
        "api_ok": last.ok, "api_errors": [e for c in calls for e in c.errors],
        "schema_valid": None if version == "v1" else parsed is not None,
        "schema_error": schema_error, "schema_retry_used": len(calls) > 1,
        "parsed_output": parsed.model_dump() if parsed else None,
        "rule_flags": [asdict(f) for f in rule_result.flags] if rule_result else [],
        "rules_fired": [f.rule_id for f in rule_result.flags if f.status == FIRED] if rule_result else [],
        "rule_primary_route": rule_result.primary_route if rule_result else None,
        "model_route": model_route, "final_route": final_route,
        "final_required_approvals": approvals,
        "model_disagreed_with_rules": disagreed,
        "sources_provided": list(sources),
        "sources_cited": list(parsed.sources_cited) if parsed else [],
        "guardrails": check_draft(draft, injection_present),
        "source_checks": check_sources(list(parsed.sources_cited), set(KB), f"{draft} {note}") if parsed else None,
        "input_tokens": sum(c.input_tokens for c in calls),
        "output_tokens": sum(c.output_tokens for c in calls),
        "cost_usd": sum(c.cost_usd or 0 for c in calls),
        "latency_seconds": round(sum(c.latency_seconds for c in calls), 3),
        "api_calls": len(calls),
    }
