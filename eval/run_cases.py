"""Run selected cases through prompt versions and write a side-by-side report.

Example (Checkpoint 2):
  python -m eval.run_cases --cases CS-5246 CS-5229 CS-5244 --versions v1 v2 v3 v4 --mode both --model small
Add --dry-run to render prompts without calling any API.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from eval.guards import GuardError, check_holdout, check_simulated_messages, check_spend, estimate_calls, split_of
from eval.split import load_cases
from src import config
from src.pipeline import VERSIONS, build_inputs, run_case

ROOT = Path(__file__).resolve().parent.parent
MESSAGES_CSV = ROOT / "data" / "simulated_messages.csv"


def load_messages() -> dict[str, str]:
    with MESSAGES_CSV.open(newline="", encoding="utf-8") as fh:
        return {r["case_id"]: r["message"] for r in csv.DictReader(fh)}


def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--cases", nargs="+", required=True)
    p.add_argument("--versions", nargs="+", default=list(VERSIONS), choices=VERSIONS)
    p.add_argument("--mode", choices=("fields", "message", "both"), default="fields")
    p.add_argument("--model", choices=sorted(config.MODELS), default="small")
    p.add_argument("--holdout", action="store_true")
    p.add_argument("--final", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def summary_line(r: dict) -> str:
    g = r["guardrails"]
    flagged = [k for k, v in g.items() if k != "violation_count" and v]
    p = r["parsed_output"] or {}
    return (f"api_ok={r['api_ok']} schema_valid={r['schema_valid']} retry={r['schema_retry_used']} | "
            f"model_route={r['model_route']} | final_route={r['final_route']} | "
            f"rules_fired={r['rules_fired'] or '-'} | disagreed={r['model_disagreed_with_rules']} | "
            f"approvals={r['final_required_approvals'] or '-'} | confidence={p.get('confidence')} | "
            f"cited={r['sources_cited'] or '-'} | guardrail_hits={flagged or 'none'} | "
            f"tokens={r['input_tokens']}/{r['output_tokens']} cost=${r['cost_usd']:.4f} "
            f"latency={r['latency_seconds']}s")


def write_report(records: list[dict], path: Path, header: str) -> None:
    out = [f"# {path.stem}", "", header, ""]
    out += ["| Case | Mode | Version | Model route | Final route | Approvals | Schema valid | Guardrail hits |",
            "|---|---|---|---|---|---|---|---|"]
    for r in records:
        out.append(f"| {r['case_id']} | {r['mode']} | {r['prompt_version']} | {r['model_route']} | "
                   f"{r['final_route']} | {', '.join(r['final_required_approvals']) or '-'} | "
                   f"{r['schema_valid']} | {r['guardrails']['violation_count']} |")
    for r in records:
        out += ["", f"## {r['case_id']} | {r['mode']} | {r['prompt_version']} ({r['model']})", "",
                summary_line(r), ""]
        for i, raw in enumerate(r["raw_outputs"], 1):
            out += [f"Raw output (call {i}):", "", "```", raw.strip() or "(empty)", "```", ""]
        if r["api_errors"]:
            out += [f"API errors: {r['api_errors']}", ""]
    path.write_text("\n".join(out), encoding="utf-8")


def main(argv=None) -> None:
    args = parse_args(argv)
    cases = {r["case_id"]: r for r in load_cases()}
    unknown = [c for c in args.cases if c not in cases]
    if unknown:
        raise SystemExit(f"Unknown case ids: {unknown}")
    modes = {"fields": [False], "message": [True], "both": [False, True]}[args.mode]
    messages = load_messages() if True in modes else {}
    splits = split_of(args.cases)
    try:
        if messages:
            check_simulated_messages(messages, cases)
        warnings = check_holdout(args.cases, args.holdout, args.final)
        expected, upper = estimate_calls(len(args.cases), args.versions, len(modes))
        check_spend(expected, upper, args.yes)
    except GuardError as exc:
        raise SystemExit(f"Refused: {exc}")

    spec = config.MODELS[args.model]
    if args.dry_run:
        for cid in args.cases:
            for with_msg in modes:
                for v in args.versions:
                    prompt, user, *_ = build_inputs(v, cases[cid], messages.get(cid) if with_msg else None)
                    print(f"\n===== {cid} {v} message={with_msg} prompt_hash={prompt.sha256} =====\n"
                          f"[SYSTEM]\n{prompt.system}\n\n[USER]\n{user}")
        return

    from src.llm import make_client
    client = make_client(args.model)
    run_id = f"run_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{args.model}"
    log_path = ROOT / "runs" / f"{run_id}.jsonl"
    records = []
    with log_path.open("w", encoding="utf-8") as log:
        for w in warnings:
            log.write(json.dumps({"run": run_id, "warning": w}) + "\n")
        for cid in args.cases:
            for with_msg in modes:
                for v in args.versions:
                    msg = messages[cid] if with_msg else None
                    rec = {"run": run_id, **run_case(cases[cid], v, client, splits[cid], msg)}
                    log.write(json.dumps(rec) + "\n")
                    log.flush()
                    records.append(rec)
                    print(f"{cid} {v} {rec['mode']}: {summary_line(rec)}")

    header = (f"Data split: {sorted(set(splits.values()))} | Mode: {args.mode} "
              f"(messages are SIMULATED) | Prompt versions: {', '.join(args.versions)} | "
              f"Model: {spec['name']} ({spec['provider']}) | Cases: {len(args.cases)} | Run log: runs/{run_id}.jsonl")
    report = ROOT / "results" / f"{run_id}_side_by_side.md"
    write_report(records, report, header)
    failures = sum(1 for r in records if not r["api_ok"] or r["schema_valid"] is False)
    print(f"\nWrote {log_path.relative_to(ROOT)} and {report.relative_to(ROOT)}. "
          f"Records: {len(records)}. API or schema failures: {failures}. "
          f"Total cost: ${sum(r['cost_usd'] for r in records):.4f}")


if __name__ == "__main__":
    main()
