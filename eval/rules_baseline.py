"""Checkpoint 1: rules only router against assigned_owner.

Run:  python -m eval.rules_baseline
Writes a JSONL run log to runs/ and summaries to results/.
No LLM is used. Text facts come from the Stage 1 keyword reader.
"""
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from eval.split import load_cases, load_split
from src.case_facts import from_csv_row
from src.rules import ALL_RULE_IDS, CLIENT_RULE_IDS, FIRED, RULES, evaluate

ROOT = Path(__file__).resolve().parent.parent
MODE = "structured fields plus keyword extraction from policy_relevant_facts (no customer message, no LLM)"

WITHOUT_PROPOSED = CLIENT_RULE_IDS | {"W1"}
WITH_PROPOSED = ALL_RULE_IDS
CONFIGS = (
    ("client_only", CLIENT_RULE_IDS, "9 client rules only"),
    ("without_proposed", WITHOUT_PROPOSED, "Client rules + W1 (without team proposed)"),
    ("plus_T1", WITHOUT_PROPOSED | {"T1"}, "Client rules + W1 + T1 fulfillment error"),
    ("plus_T2", WITHOUT_PROPOSED | {"T2"}, "Client rules + W1 + T2 stalled shipment"),
    ("with_proposed", WITH_PROPOSED, "Client rules + W1 + T1 + T2 (with team proposed)"),
)


def header(split: str, n: int) -> str:
    return (f"Data split: {split} | Mode: {MODE} | Prompt version: none (rules only) "
            f"| Model: none | Cases: {n}")


def run() -> tuple[list[dict], str]:
    cases = load_cases()
    split_of = {cid: "tune" for cid in load_split("tune")}
    split_of.update({cid: "holdout" for cid in load_split("holdout")})
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    records = []
    for row in cases:
        facts = from_csv_row(row)
        for name, enabled, _ in CONFIGS:
            result = evaluate(facts, enabled)
            records.append({
                "timestamp": ts, "run": f"rules_baseline_{ts}", "config": name,
                "enabled_rules": sorted(enabled), "case_id": row["case_id"],
                "split": split_of[row["case_id"]], "mode": MODE,
                "prompt_version": None, "model": None, "provider": None,
                "input_facts": asdict(facts), "rule_flags": [asdict(f) for f in result.flags],
                "primary_route": result.primary_route,
                "required_approvals": list(result.required_approvals),
                "assigned_owner": row["assigned_owner"],
                "match": result.primary_route == row["assigned_owner"],
            })
    return records, ts


def write_log(records: list[dict], ts: str) -> Path:
    path = ROOT / "runs" / f"rules_baseline_{ts}.jsonl"
    path.parent.mkdir(exist_ok=True)
    warning = {"timestamp": ts, "warning": "HOLDOUT TOUCHED: rules only baseline evaluated on holdout "
               "cases at user request. Rules are deterministic and were not tuned in this run."}
    with path.open("w", encoding="utf-8") as fh:
        for rec in [warning, *records]:
            fh.write(json.dumps(rec) + "\n")
    return path


def rate(recs: list[dict]) -> str:
    hits = sum(r["match"] for r in recs)
    return f"{hits}/{len(recs)} ({100 * hits / len(recs):.1f}%)"


def summary_table(records: list[dict]) -> list[str]:
    lines = ["| Config | All 48 | Tune 28 | Holdout 20 |", "|---|---|---|---|"]
    for name, _, label in CONFIGS:
        recs = [r for r in records if r["config"] == name]
        cells = [rate(recs)] + [rate([r for r in recs if r["split"] == s]) for s in ("tune", "holdout")]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return lines


def mismatch_table(records: list[dict], config: str) -> list[str]:
    lines = ["| Case | Split | assigned_owner | Rules primary_route | Fired rules | Required approvals |",
             "|---|---|---|---|---|---|"]
    for r in records:
        if r["config"] == config and not r["match"]:
            fired = ", ".join(f["rule_id"] for f in r["rule_flags"] if f["status"] == FIRED) or "none (default)"
            lines.append(f"| {r['case_id']} | {r['split']} | {r['assigned_owner']} | {r['primary_route']} "
                         f"| {fired} | {', '.join(r['required_approvals']) or '-'} |")
    return lines


def rule_counts(records: list[dict]) -> list[str]:
    recs = [r for r in records if r["config"] == "with_proposed"]
    lines = ["| Rule | Origin | Fired | Not fired | Cannot evaluate |", "|---|---|---|---|---|"]
    for rule in RULES:
        statuses = [f["status"] for r in recs for f in r["rule_flags"] if f["rule_id"] == rule.id]
        counts = [statuses.count(s) for s in ("fired", "not_fired", "cannot_evaluate")]
        lines.append(f"| {rule.id} | {rule.origin} | " + " | ".join(map(str, counts)) + " |")
    return lines


def write_results(records: list[dict], log_path: Path) -> str:
    md = [
        "# Checkpoint 1: rules only router vs assigned_owner", "",
        header("all 48 (tune 28 + holdout 20)", 48), "",
        f"Run log: `{log_path.relative_to(ROOT).as_posix()}`. The label is `assigned_owner`, a current "
        "process step, not an approved final action. The sample is not representative. The rules were "
        "developed with knowledge of all 48 cases, so holdout numbers are not an unbiased estimate.", "",
        "## Match rate", "", *summary_table(records), "",
        "## Mismatches without team proposed rules (client rules + W1)", "",
        header("all 48", 48), "", *mismatch_table(records, "without_proposed"), "",
        "## Mismatches with team proposed rules (client rules + W1 + T1 + T2)", "",
        header("all 48", 48), "", *mismatch_table(records, "with_proposed"), "",
        "## Rule status counts (with team proposed config)", "",
        header("all 48", 48), "", *rule_counts(records), "",
    ]
    text = "\n".join(md)
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "rules_baseline.md").write_text(text, encoding="utf-8")
    write_case_csv(records)
    return text


def write_case_csv(records: list[dict]) -> None:
    by_case: dict[str, dict] = {}
    for r in records:
        row = by_case.setdefault(r["case_id"], {
            "case_id": r["case_id"], "split": r["split"], "mode": MODE,
            "issue_type": r["input_facts"]["issue_type"], "assigned_owner": r["assigned_owner"]})
        row[f"route_{r['config']}"] = r["primary_route"]
        row[f"match_{r['config']}"] = r["match"]
        if r["config"] == "with_proposed":
            row["fired_with_proposed"] = " ".join(f["rule_id"] for f in r["rule_flags"] if f["status"] == FIRED)
            row["approvals_with_proposed"] = "; ".join(r["required_approvals"])
    rows = list(by_case.values())
    with (ROOT / "results" / "rules_baseline_cases.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    records, ts = run()
    log_path = write_log(records, ts)
    print(write_results(records, log_path))


if __name__ == "__main__":
    main()
