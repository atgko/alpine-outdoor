"""Metrics for one or more run logs (brief section 7.3). No API calls.

  py -3.14 -m eval.metrics runs/a.jsonl runs/b.jsonl --name checkpoint3

Writes results/<name>_metrics.md (tables per model and mode, one column per
prompt version), results/<name>_cases.csv (one row per record) and
results/<name>_failures.md (worst records with raw output).

Guardrails are recomputed with the current src/guardrails.py on customer facing
text, so runs made with older checks are judged the same way. The logged
values stay in the run logs.

Labels:
- Route accuracy uses assigned_owner, a process label, not ground truth.
- The policy-consistent view uses eval/policy_labels.json overrides.
- Expected approvals: assigned_owner when it is not Support Representative,
  plus Support Lead when rule 7 applies (amount over $500 and a refund or
  replacement is requested). v4 and v5 copy rule layer approvals, so their
  recall is partly true by construction.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from eval.rescore_guardrails import load_records, rescore
from eval.split import SEED, load_cases
from src.case_facts import ISSUE_TYPE_MAP
from src.guardrails import VIOLATION_CHECKS, WARNING_CHECKS
from src.rules import FINANCIAL_OUTCOMES, HIGH_VALUE_USD, LEAD, REP, SAFETY

ROOT = Path(__file__).resolve().parent.parent
POLICY_LABELS = ROOT / "eval" / "policy_labels.json"
EXTRACTION_SUBSET_SIZE = 15
WORST_FAILURES_SHOWN = 10
GROUNDED_VERSIONS = {"v3", "v4", "v5"}
HYBRID_VERSIONS = {"v4", "v5"}


def policy_routes() -> dict[str, str]:
    overrides = json.loads(POLICY_LABELS.read_text(encoding="utf-8"))["overrides"]
    return {cid: o["route"] for cid, o in overrides.items()}


def expected_approvals(row: dict) -> set[str]:
    expected = {row["assigned_owner"]} - {REP}
    amount = float(row["purchase_amount_usd"] or 0)
    if amount > HIGH_VALUE_USD and row["requested_outcome"] in FINANCIAL_OUTCOMES:
        expected.add(LEAD)
    return expected


def extraction_subset(case_ids) -> set[str]:
    """A fixed sample of up to 15 cases per split, drawn with the split seed."""
    ids = sorted(set(case_ids))
    return set(random.Random(SEED).sample(ids, min(EXTRACTION_SUBSET_SIZE, len(ids))))


def is_safety_case(row: dict) -> bool:
    return row["assigned_owner"] == SAFETY or row["issue_type"] == "Product safety concern"


def order_flagged(parsed: dict) -> bool:
    asks = any(re.search(r"order", m, re.I) for m in parsed["missing_information"])
    return parsed["order_number_present"] is False or asks


def case_result(r: dict, row: dict, policy_route: str, in_subset: bool) -> dict:
    """Flatten one run record into the scored row written to the CSV."""
    p = r["parsed_output"]
    route = r["final_route"]
    g, text_source = rescore(r)
    expected = expected_approvals(row)
    has_approvals = p is not None
    sc = r.get("source_checks") or {}
    out = {
        "run": r["run"], "case_id": r["case_id"], "split": r["split"], "mode": r["mode"],
        "version": r["prompt_version"], "provider": r["provider"], "model": r["model"],
        "repeat": r.get("repeat", 1), "csv_issue_type": row["issue_type"],
        "api_ok": r["api_ok"], "schema_valid": r["schema_valid"],
        "final_route": route, "model_route": r["model_route"],
        "assigned_owner": row["assigned_owner"], "owner_match": route == row["assigned_owner"],
        "policy_route": policy_route, "policy_match": route == policy_route,
        "expected_approvals": "; ".join(sorted(expected)),
        "approvals": "; ".join(r["final_required_approvals"]),
        "approval_recall_ok": (expected <= set(r["final_required_approvals"])) if expected and has_approvals else None,
        "no_order_case": row["order_number_provided"] == "No",
        "missing_order_flagged": order_flagged(p) if p and row["order_number_provided"] == "No" else None,
        "extract_issue_type_ok": None, "extract_order_ok": None, "extract_category_ok": None,
        "sources_cited": "; ".join(r["sources_cited"]),
        "unknown_source_ids": "; ".join(sc.get("unknown_ids", [])),
        "kb710_without_caveat": sc.get("kb710_without_caveat"),
        "safety_case": is_safety_case(row), "safety_routed_ok": route == SAFETY if is_safety_case(row) else None,
        "model_disagreed_with_rules": r["model_disagreed_with_rules"],
        "guardrail_text": text_source, "violation_count": g["violation_count"],
        "violations": "; ".join(k for k in VIOLATION_CHECKS if g[k]),
        "warning_count": g["warning_count"], "warnings": "; ".join(k for k in WARNING_CHECKS if g[k]),
        "cost_usd": r["cost_usd"], "latency_seconds": r["latency_seconds"],
    }
    if p and in_subset:
        out["extract_issue_type_ok"] = p["issue_type"] == ISSUE_TYPE_MAP.get(row["issue_type"], "other")
        out["extract_order_ok"] = p["order_number_present"] == (row["order_number_provided"] == "Yes")
        out["extract_category_ok"] = row["product_category"].lower() in p["product_category"].lower()
    for check in VIOLATION_CHECKS + WARNING_CHECKS:
        out[f"g_{check}"] = bool(g[check])
    return out


def score_records(records: list[dict]) -> list[dict]:
    cases = {c["case_id"]: c for c in load_cases()}
    policy = policy_routes()
    unknown = sorted({r["case_id"] for r in records} - set(cases))
    if unknown:
        raise SystemExit(f"Records for cases not in the CSV (for example adversarial cases): {unknown}. "
                         "Adversarial scoring is not built yet.")
    by_split = defaultdict(set)
    for r in records:
        by_split[r["split"]].add(r["case_id"])
    subsets = {s: extraction_subset(ids) for s, ids in by_split.items()}
    return [case_result(r, cases[r["case_id"]], policy.get(r["case_id"], cases[r["case_id"]]["assigned_owner"]),
                        r["case_id"] in subsets[r["split"]]) for r in records]


def ratio(rows: list[dict], key: str) -> str:
    """'k/n (pct)' over rows where the value is not None, or 'n/a'."""
    vals = [row[key] for row in rows if row[key] is not None]
    return f"{sum(vals)}/{len(vals)} ({100 * sum(vals) / len(vals):.0f}%)" if vals else "n/a"


def count(rows: list[dict], key: str) -> str:
    return f"{sum(bool(row[key]) for row in rows)}/{len(rows)}" if rows else "n/a"


METRIC_ROWS = (
    ("API ok", lambda rs: ratio(rs, "api_ok")),
    ("Schema valid (v2 onwards)", lambda rs: ratio(rs, "schema_valid")),
    ("Route = assigned_owner", lambda rs: ratio(rs, "owner_match")),
    ("Route = policy-consistent label", lambda rs: ratio(rs, "policy_match")),
    ("Required approval recall", lambda rs: ratio(rs, "approval_recall_ok")),
    ("No order number flagged", lambda rs: ratio(rs, "missing_order_flagged")),
    ("Extraction: issue_type (15 case subset)", lambda rs: ratio(rs, "extract_issue_type_ok")),
    ("Extraction: order_number_present", lambda rs: ratio(rs, "extract_order_ok")),
    ("Extraction: product_category", lambda rs: ratio(rs, "extract_category_ok")),
    ("Cited ids unknown (v3 onwards)",
     lambda rs: count([r for r in rs if r["version"] in GROUNDED_VERSIONS], "unknown_source_ids")),
    ("KB-710 cited without caveat (v3 onwards)",
     lambda rs: count([r for r in rs if r["version"] in GROUNDED_VERSIONS], "kb710_without_caveat")),
    ("Safety cases routed to Product Safety", lambda rs: ratio(rs, "safety_routed_ok")),
    ("Model disagreed with rules (v4, v5)",
     lambda rs: count([r for r in rs if r["version"] in HYBRID_VERSIONS], "model_disagreed_with_rules")),
    ("Records with a guardrail violation", lambda rs: count(rs, "violations")),
    *((f"  {c}", lambda rs, c=c: count(rs, f"g_{c}")) for c in VIOLATION_CHECKS),
    ("Records with a warning (not a violation)", lambda rs: count(rs, "warnings")),
    *((f"  {c}", lambda rs, c=c: count(rs, f"g_{c}")) for c in WARNING_CHECKS),
    ("Mean latency per call (s)", lambda rs: f"{sum(r['latency_seconds'] for r in rs) / len(rs):.1f}"),
    ("Mean cost per record (USD)", lambda rs: f"{sum(r['cost_usd'] for r in rs) / len(rs):.4f}"),
    ("Total cost (USD)", lambda rs: f"{sum(r['cost_usd'] for r in rs):.4f}"),
)


def group(rows: list[dict], *keys: str) -> dict[tuple, list[dict]]:
    out = defaultdict(list)
    for row in rows:
        out[tuple(row[k] for k in keys)].append(row)
    return dict(sorted(out.items()))


def header(rows: list[dict], provider: str, model: str, mode: str, versions: list[str]) -> str:
    splits = ", ".join(sorted({r["split"] for r in rows}))
    sim = " (messages are SIMULATED)" if mode != "fields_only" else ""
    n_cases = len({r["case_id"] for r in rows})
    return (f"Data split: {splits} | Mode: {mode}{sim} | Prompt versions: {', '.join(versions)} | "
            f"Model: {model} ({provider}) | Cases: {n_cases} | Records: {len(rows)}")


def metrics_tables(rows: list[dict]) -> list[str]:
    out = []
    for (provider, model, mode), rs in group(rows, "provider", "model", "mode").items():
        by_version = group(rs, "version")
        versions = [v for (v,) in by_version]
        out += ["", f"## {model} | {mode}", "", header(rs, provider, model, mode, versions), "",
                "| Metric | " + " | ".join(versions) + " |", "|---|" + "---|" * len(versions)]
        out += [f"| {name} | " + " | ".join(fn(by_version[(v,)]) for v in versions) + " |"
                for name, fn in METRIC_ROWS]
        out += ["", f"Route = assigned_owner by CSV issue type ({model}, {mode}):", "",
                "| Issue type | " + " | ".join(versions) + " |", "|---|" + "---|" * len(versions)]
        for (issue,), issue_rows in group(rs, "csv_issue_type").items():
            per_v = group(issue_rows, "version")
            out.append(f"| {issue} | " + " | ".join(ratio(per_v.get((v,), []), "owner_match") for v in versions) + " |")
    return out


def consistency(rows: list[dict]) -> list[str]:
    """Route and guardrail changes across repeated runs of the same case, version, mode and model."""
    repeated = {k: rs for k, rs in group(rows, "model", "mode", "version", "case_id").items() if len(rs) > 1}
    if not repeated:
        return ["", "## Consistency", "", "No repeated runs in these logs (use run_eval --repeats 3)."]
    summary = defaultdict(lambda: [0, 0, 0])  # case groups, route changed, violations changed
    for (model, mode, version, _case), rs in repeated.items():
        s = summary[(model, mode, version)]
        s[0] += 1
        s[1] += len({r["final_route"] for r in rs}) > 1
        s[2] += len({r["violations"] for r in rs}) > 1
    out = ["", "## Consistency", "", "| Model | Mode | Version | Case groups | Route changed | Violations changed |",
           "|---|---|---|---|---|---|"]
    out += [f"| {m} | {mode} | {v} | {n} | {routes} | {guards} |"
            for (m, mode, v), (n, routes, guards) in sorted(summary.items())]
    return out


def severity(row: dict) -> int:
    """Higher is worse. Used only to order the failures file for manual review."""
    return (100 * (not row["api_ok"] or row["schema_valid"] is False) + 50 * (row["safety_routed_ok"] is False)
            + 20 * row["violation_count"] + 10 * (not row["policy_match"]) + 5 * (not row["owner_match"])
            + 2 * (row["approval_recall_ok"] is False) + row["warning_count"])


def failures(rows: list[dict], records: list[dict]) -> list[str]:
    raw = {(r["run"], r["case_id"], r["mode"], r["prompt_version"], r.get("repeat", 1)): r for r in records}
    worst = sorted((r for r in rows if severity(r) > 0), key=severity, reverse=True)[:WORST_FAILURES_SHOWN]
    out = ["# Worst records for manual review", "",
           f"Ordered by a simple severity score (see eval/metrics.py). Top {WORST_FAILURES_SHOWN} of "
           f"{sum(severity(r) > 0 for r in rows)} records with any failure.", ""]
    for row in worst:
        rec = raw[(row["run"], row["case_id"], row["mode"], row["version"], row["repeat"])]
        out += [f"## {row['case_id']} | {row['mode']} | {row['version']} | severity {severity(row)}", "",
                f"route={row['final_route']} owner={row['assigned_owner']} policy={row['policy_route']} | "
                f"approvals={row['approvals'] or '-'} (expected {row['expected_approvals'] or '-'}) | "
                f"violations={row['violations'] or '-'} | warnings={row['warnings'] or '-'} | "
                f"api_ok={row['api_ok']} schema_valid={row['schema_valid']}", "",
                "```", (rec["raw_outputs"][-1] if rec["raw_outputs"] else "(no output)").strip(), "```", ""]
    return out


def write_reports(log_paths: list[Path], name: str) -> Path:
    records = [r for p in log_paths for r in load_records(p)]
    rows = score_records(records)
    logs = ", ".join(p.as_posix() for p in log_paths)
    md = [f"# Metrics: {name}", "",
          f"Run logs: {logs}. Every number comes from these logs. Guardrails recomputed with the current "
          "src/guardrails.py. assigned_owner is a process label, not ground truth. The 48 cases are a "
          "selected sample, not representative.", *metrics_tables(rows), *consistency(rows)]
    results = ROOT / "results"
    (results / f"{name}_metrics.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (results / f"{name}_failures.md").write_text("\n".join(failures(rows, records)) + "\n", encoding="utf-8")
    with (results / f"{name}_cases.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return results / f"{name}_metrics.md"


def expand(patterns: list[str]) -> list[Path]:
    """Expand wildcards here, because PowerShell passes them to Python unexpanded."""
    paths = []
    for pattern in patterns:
        matches = sorted(Path().glob(pattern)) if any(ch in pattern for ch in "*?[") else [Path(pattern)]
        if not matches:
            raise SystemExit(f"No run logs match {pattern}")
        paths += matches
    return paths


def main(argv=None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("logs", nargs="+", help="run log paths; wildcards allowed")
    p.add_argument("--name", required=True, help="prefix for the files in results/")
    args = p.parse_args(argv)
    paths = expand(args.logs)
    print("Run logs: " + ", ".join(p.as_posix() for p in paths))
    print(f"Wrote {write_reports(paths, args.name).relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
