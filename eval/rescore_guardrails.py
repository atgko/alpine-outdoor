"""Re-run the current guardrail checks on a saved run log. No API calls.

  py -3.14 -m eval.rescore_guardrails runs/run_20261030T224609Z_small.jsonl

The run log is not modified. Writes results/<run>_guardrails_rescored.md with
the logged (old) and recomputed (new) counts for every record.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from src.guardrails import VIOLATION_CHECKS, WARNING_CHECKS, check_draft, customer_text

ROOT = Path(__file__).resolve().parent.parent


def load_records(path: Path) -> list[dict]:
    """Case records from a run log (warning lines are skipped)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [r for r in map(json.loads, filter(None, lines)) if "case_id" in r]


def rescore(record: dict) -> tuple[dict, str]:
    parsed = record.get("parsed_output") or {}
    raw = record["raw_outputs"][-1] if record.get("raw_outputs") else ""
    text, source = customer_text(record["prompt_version"], parsed.get("draft_reply"), raw)
    return check_draft(text, record.get("injection_present", False)), source


def hits(g: dict, checks: tuple[str, ...]) -> str:
    return "; ".join(f"{k}: {', '.join(g[k])}" for k in checks if g.get(k)) or "-"


def main(argv=None) -> None:
    path = Path((argv or sys.argv[1:])[0])
    records = load_records(path)
    rows, old_total, new_total, warn_total = [], 0, 0, 0
    for r in records:
        new, source = rescore(r)
        old_hits = "; ".join(f"{k}: {', '.join(v)}" for k, v in r["guardrails"].items()
                             if isinstance(v, list) and v) or "-"
        old_total += r["guardrails"]["violation_count"]
        new_total += new["violation_count"]
        warn_total += new["warning_count"]
        rows.append(f"| {r['case_id']} | {r['mode']} | {r['prompt_version']} | {source} | "
                    f"{r['guardrails']['violation_count']} | {old_hits} | {new['violation_count']} | "
                    f"{hits(new, VIOLATION_CHECKS)} | {new['warning_count']} | {hits(new, WARNING_CHECKS)} |")
    out = [f"# Guardrail rescoring: {path.stem}", "",
           f"Run log: {path.as_posix()} (not modified). Records: {len(records)}. No API calls. "
           "Old = counts logged at run time. New = current src/guardrails.py on customer facing text only.", "",
           f"Totals: old violations {old_total}, new violations {new_total}, new warnings {warn_total}.", "",
           "| Case | Mode | Version | Text checked | Old violations | Old hits | New violations | New hits "
           "| New warnings | Warning hits |",
           "|---|---|---|---|---|---|---|---|---|---|", *rows]
    report = ROOT / "results" / f"{path.stem}_guardrails_rescored.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Old violations {old_total}, new violations {new_total}, new warnings {warn_total}. "
          f"Wrote {report.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
