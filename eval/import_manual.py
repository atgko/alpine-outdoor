"""Import outputs pasted from a chat window (manual spot check) and score them.

  py -3.14 -m eval.import_manual spot_check.csv --tool ChatGPT

Input CSV (template: eval/manual_spot_check_template.csv), one row per case:
  case_id             required, a CSV case id
  output              the full answer as pasted. If it is a JSON object that
                      matches the schema, all fields are used.
  draft_reply         optional: only the customer reply, if pasted separately
  recommended_route   optional: overrides the route read from the output
  required_approvals  optional: route names separated by ";"
  model               optional: model name shown in the chat tool
  prompt_version      optional: which prompt was pasted (default "manual")

No API calls. The rows become a run log in runs/manual_<time>.jsonl with
mode "manual spot check", and are scored by eval/metrics.py with the same
route and guardrail checks as API runs. Cost and latency are not known and
are logged as 0. Holdout cases need --holdout --final, as for API runs.

Guardrails check, in order: the JSON draft_reply, else the draft_reply column,
else the whole pasted output (only the "Draft reply" section if
prompt_version is v1). Paste the reply into draft_reply to keep routing notes
out of the check.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from eval.guards import GuardError, check_holdout, split_of
from eval.metrics import write_reports
from eval.split import load_cases
from src.guardrails import check_draft, check_sources, customer_text
from src.kb import load_kb
from src.pipeline import route_from_text
from src.schema import ROUTES, parse_output

ROOT = Path(__file__).resolve().parent.parent
MODE = "manual spot check"


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in csv.DictReader(fh)]
    if not rows:
        raise SystemExit(f"{path} has no rows")
    problems = []
    cases = {c["case_id"] for c in load_cases()}
    for i, r in enumerate(rows, 2):  # line 1 is the header
        if r.get("case_id") not in cases:
            problems.append(f"line {i}: unknown case_id {r.get('case_id')!r}")
        if not (r.get("output") or r.get("draft_reply")):
            problems.append(f"line {i}: needs output or draft_reply")
        for route in [r.get("recommended_route", "")] + r.get("required_approvals", "").split(";"):
            if route.strip() and route.strip() not in ROUTES:
                problems.append(f"line {i}: unknown route {route.strip()!r}")
    if problems:
        raise SystemExit("Manual CSV refused: " + "; ".join(problems))
    return rows


def to_record(row: dict, run_id: str, tool: str, split: str, known_ids: set[str]) -> dict:
    """Shape one pasted answer like a pipeline run record so metrics.py can score it."""
    version = row.get("prompt_version") or "manual"
    output = row.get("output", "")
    is_json = output.lstrip().startswith(("{", "```"))
    parsed, schema_error = parse_output(output) if is_json else (None, None)
    p = parsed.model_dump() if parsed else None
    # metrics.py checks raw_outputs[-1] when there is no parsed JSON, so a
    # separately pasted reply goes last.
    raw_outputs = [o for o in (output, row.get("draft_reply") if not p else "") if o]
    route = row.get("recommended_route") or (p["recommended_route"] if p else route_from_text(raw_outputs[0]))
    approvals_text = row.get("required_approvals", "")
    approvals = [a.strip() for a in approvals_text.split(";") if a.strip()] if approvals_text \
        else (p["required_approvals"] if p else [])
    draft, source = customer_text(version, p["draft_reply"] if p else None, raw_outputs[-1])
    cited = p["sources_cited"] if p else []
    return {
        "run": run_id, "repeat": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "prompt_version": version, "prompt_hash": None, "provider": tool, "model": row.get("model") or tool,
        "case_id": row["case_id"], "split": split, "mode": MODE, "input": None,
        "raw_outputs": raw_outputs, "api_ok": True, "api_errors": [],
        "schema_valid": (parsed is not None) if is_json else None,
        "schema_error": schema_error, "schema_retry_used": False, "parsed_output": p,
        "rule_flags": [], "rules_fired": [], "rule_primary_route": None,
        "model_route": route, "final_route": route, "final_required_approvals": approvals,
        "model_disagreed_with_rules": None, "sources_provided": [], "sources_cited": cited,
        "injection_present": False, "guardrail_text_source": source, "guardrails": check_draft(draft),
        "source_checks": check_sources(cited, known_ids, f"{draft} {p['draft_case_note'] if p else ''}") if p else None,
        "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "latency_seconds": 0.0, "api_calls": 0,
    }


def import_manual(csv_path: Path, tool: str, holdout: bool = False, final: bool = False,
                  runs_dir: Path = ROOT / "runs") -> tuple[Path, list[dict]]:
    rows = read_rows(csv_path)
    splits = split_of([r["case_id"] for r in rows])
    try:
        warnings = check_holdout(list(splits), holdout, final)
    except GuardError as exc:
        raise SystemExit(f"Refused: {exc}")
    run_id = f"manual_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{tool.lower().replace(' ', '-')}"
    known = set(load_kb())
    records = [to_record(r, run_id, tool, splits[r["case_id"]], known) for r in rows]
    log_path = runs_dir / f"{run_id}.jsonl"
    with log_path.open("w", encoding="utf-8") as log:
        log.write(json.dumps({"run": run_id, "note": f"manual spot check imported from {csv_path.name}"}) + "\n")
        for w in warnings:
            log.write(json.dumps({"run": run_id, "warning": w}) + "\n")
        for rec in records:
            log.write(json.dumps(rec) + "\n")
    return log_path, records


def main(argv=None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    p.add_argument("--tool", required=True, help='chat tool used, for example "ChatGPT"')
    p.add_argument("--holdout", action="store_true")
    p.add_argument("--final", action="store_true")
    args = p.parse_args(argv)
    log_path, records = import_manual(args.csv, args.tool, args.holdout, args.final)
    report = write_reports([log_path], log_path.stem)
    print(f"Imported {len(records)} rows. Wrote {log_path.relative_to(ROOT).as_posix()} and "
          f"{report.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
