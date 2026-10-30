"""Evaluation harness: run a split through prompt versions, log every call, then score it.

  py -3.14 -m eval.run_eval --split tune --versions v1 --mode both --model small
  py -3.14 -m eval.run_eval --split tune --versions v4 --mode both --dry-run

The holdout split is locked. It runs only with both --holdout and --final, and
every holdout run writes a warning line into its run log. Use --dry-run to see
the call estimate and case list without any API call. Adversarial cases are
not run by this script yet.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from eval.guards import GuardError, check_holdout, check_simulated_messages, check_spend, estimate_calls
from eval.metrics import write_reports
from eval.run_cases import load_messages, summary_line
from eval.split import load_cases, load_split
from src import config
from src.pipeline import VERSIONS, run_case

ROOT = Path(__file__).resolve().parent.parent
MODES = {"fields": [False], "message": [True], "both": [False, True]}


def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--split", choices=("tune", "holdout"), default="tune")
    p.add_argument("--cases", nargs="+", help="optional subset of the split")
    p.add_argument("--versions", nargs="+", default=list(VERSIONS), choices=VERSIONS)
    p.add_argument("--mode", choices=sorted(MODES), default="both")
    p.add_argument("--model", choices=sorted(config.MODELS), default="small")
    p.add_argument("--repeats", type=int, default=1, help="runs per case, for the consistency test")
    p.add_argument("--holdout", action="store_true")
    p.add_argument("--final", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args(argv)


def select_cases(split: str, subset: list[str] | None) -> list[str]:
    ids = load_split(split)
    if subset:
        outside = [c for c in subset if c not in ids]
        if outside:
            raise SystemExit(f"Cases not in the {split} split: {outside}")
        ids = [c for c in ids if c in subset]
    return ids


def main(argv=None) -> None:
    args = parse_args(argv)
    case_ids = select_cases(args.split, args.cases)
    cases = {r["case_id"]: r for r in load_cases()}
    modes = MODES[args.mode]
    messages = load_messages() if True in modes else {}
    try:
        warnings = check_holdout(case_ids, args.holdout, args.final)
        if messages:
            check_simulated_messages(messages, {c: cases[c] for c in case_ids})
        expected, upper = estimate_calls(len(case_ids), args.versions, len(modes), args.repeats)
        check_spend(expected, upper, args.yes)
    except GuardError as exc:
        raise SystemExit(f"Refused: {exc}")

    spec = config.MODELS[args.model]
    print(f"Split {args.split}: {len(case_ids)} cases | versions {' '.join(args.versions)} | "
          f"mode {args.mode} | model {spec['name']} | repeats {args.repeats}", flush=True)
    if args.dry_run:
        print("Dry run: no API calls made. Cases: " + " ".join(case_ids))
        return

    from src.llm import make_client
    client = make_client(args.model)
    run_id = f"eval_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}_{args.split}_{args.model}_{'-'.join(args.versions)}"
    log_path = ROOT / "runs" / f"{run_id}.jsonl"
    done, total, failed, cost = 0, expected, 0, 0.0
    with log_path.open("w", encoding="utf-8") as log:
        for w in warnings:
            log.write(json.dumps({"run": run_id, "warning": w}) + "\n")
        for repeat in range(1, args.repeats + 1):
            for cid in case_ids:
                for with_msg in modes:
                    for v in args.versions:
                        msg = messages[cid] if with_msg else None
                        rec = {"run": run_id, "repeat": repeat, **run_case(cases[cid], v, client, args.split, msg)}
                        log.write(json.dumps(rec) + "\n")
                        log.flush()
                        done += 1
                        failed += not rec["api_ok"] or rec["schema_valid"] is False
                        cost += rec["cost_usd"]
                        print(f"[{done}/{total}] {cid} {v} {rec['mode']}: {summary_line(rec)}", flush=True)

    report = write_reports([log_path], run_id)
    print(f"\nWrote {log_path.relative_to(ROOT).as_posix()} and {report.relative_to(ROOT).as_posix()} "
          f"(plus _cases.csv and _failures.md). Records: {done}. API or schema failures: {failed}. "
          f"Total cost: ${cost:.4f}", flush=True)


if __name__ == "__main__":
    main()
