"""Stage 4 review screen: a local Flask app for a human representative.

  py -3.14 -m src.review_app          then open http://127.0.0.1:5000

Draft only. The app cannot take any business action. Its buttons (Approve,
Edit, Reject) only append a line to runs/audit.jsonl.

Modes:
  Replay  shows an output recorded in a run log in runs/ (no API call)
  Live    runs the pipeline on the selected case now (needs ANTHROPIC_API_KEY,
          run it from a normal terminal). Each live call is appended to
          runs/live_<date>.jsonl like any other run.

Only tune cases and the adversarial cases are listed. Holdout cases are
never shown, and holdout records in run logs are skipped.
"""
from __future__ import annotations

import json
import os
import re
import secrets
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

from eval.run_adversarial import load_adversarial
from eval.run_cases import load_messages
from eval.split import load_cases, load_split
from src import config
from src.case_facts import from_csv_row
from src.guardrails import VIOLATION_CHECKS, WARNING_CHECKS, check_draft, customer_text
from src.kb import load_kb
from src.pipeline import FIELDS_ONLY, HYBRID, INPUT_FIELDS, VERSIONS, WITH_MESSAGE, run_case
from src.rules import evaluate

ROOT = Path(__file__).resolve().parent.parent
BANNER = "Draft only. Actions are taken by a representative in the authorized systems."
DECISIONS = ("approve", "edit", "reject")
SAFE_NAME = re.compile(r"^[\w.-]+\.(?:jsonl|md)$")
KB = load_kb()


def case_catalog() -> dict[str, dict]:
    """Tune cases and adversarial cases. Holdout cases are never included."""
    rows = {r["case_id"]: r for r in load_cases()}
    messages = load_messages()
    holdout = set(load_split("holdout"))
    catalog = {cid: {"row": rows[cid], "message": messages.get(cid), "split": "tune", "injection": False,
                     "message_label": "SIMULATED customer message (written from the case row)"}
               for cid in load_split("tune") if cid not in holdout}
    for cid, c in load_adversarial().items():
        catalog[cid] = {"row": c["case"], "message": c["message"], "split": "adversarial",
                        "injection": c["injection_present"], "title": c["title"],
                        "message_label": "Hand written adversarial message (SIMULATED)"}
    return catalog


def safe_file(folder: Path, name: str, suffix: str) -> Path:
    """Only plain file names inside the folder; anything else is a 404."""
    if not name or not SAFE_NAME.match(name) or not name.endswith(suffix):
        abort(404)
    path = folder / name
    if not path.is_file():
        abort(404)
    return path


def index_runs(runs_dir: Path, allowed: set[str]) -> dict[str, list[dict]]:
    """Recorded outputs per case: {case_id: [{file, line, version, mode, split, timestamp}]}, newest first."""
    found: dict[str, list[dict]] = {}
    for path in sorted(runs_dir.glob("*.jsonl")):
        if path.name == "audit.jsonl":
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            if '"raw_outputs"' not in line:
                continue
            r = json.loads(line)
            if r.get("case_id") in allowed and r.get("split") != "holdout":
                found.setdefault(r["case_id"], []).append(
                    {"file": path.name, "line": line_no, "version": r["prompt_version"], "mode": r["mode"],
                     "model": r.get("model"), "split": r.get("split"), "timestamp": r.get("timestamp", "")})
    for records in found.values():
        records.sort(key=lambda x: (x["timestamp"], x["file"], x["line"]), reverse=True)
    return found


def load_record(runs_dir: Path, name: str, line: int, case_id: str) -> dict:
    path = safe_file(runs_dir, name, ".jsonl")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not 0 <= line < len(lines):
        abort(404)
    record = json.loads(lines[line])
    if record.get("case_id") != case_id or record.get("split") == "holdout":
        abort(400, "The record does not belong to the selected case.")
    return record


def rule_view(record: dict, row: dict) -> tuple[list[dict], str]:
    if record.get("prompt_version") in HYBRID and record.get("rule_flags"):
        return record["rule_flags"], "Rule layer results recorded in this run (mandatory facts for the model)."
    flags = [asdict(f) for f in evaluate(from_csv_row(row)).flags]
    return flags, ("This prompt version does not use the rule layer. Shown for reference: rule layer "
                   "computed now from the case fields, not part of the recorded output.")


def record_view(record: dict, row: dict) -> dict:
    parsed = record.get("parsed_output")
    raw = record["raw_outputs"][-1] if record.get("raw_outputs") else ""
    draft, text_source = customer_text(record["prompt_version"], parsed["draft_reply"] if parsed else None, raw)
    guard = check_draft(draft, record.get("injection_present", False))
    flags, flags_note = rule_view(record, row)
    facts = {k: v for k, v in asdict(from_csv_row(row)).items() if k not in ("sources", "case_id")}
    return {
        "record": record, "parsed": parsed, "raw": raw, "draft": draft, "draft_source": text_source,
        "flags": flags, "flags_note": flags_note, "rule_facts": facts,
        "sources": [{"id": s, "kb": KB.get(s)} for s in record.get("sources_cited", [])],
        "violations": {k: guard[k] for k in VIOLATION_CHECKS if guard[k]},
        "warnings": {k: guard[k] for k in WARNING_CHECKS if guard[k]},
    }


def markdown_blocks(text: str) -> list[dict]:
    """Minimal markdown reader for results files: headings, tables, code blocks, text.
    Cell text is shown exactly as written in the file (escaped by the template)."""
    blocks: list[dict] = []
    lines, i = text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            blocks.append({"type": "code", "text": "\n".join(lines[i + 1:j])})
            i = j + 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append({"type": "table", "header": rows[0], "rows": rows[1:]})
        elif m := re.match(r"(#{1,4})\s+(.*)", line):
            blocks.append({"type": "heading", "level": len(m.group(1)) + 1, "text": m.group(2)})
            i += 1
        elif line.strip():
            blocks.append({"type": "text", "text": line})
            i += 1
        else:
            i += 1
    return blocks


def create_app(runs_dir: Path = ROOT / "runs", results_dir: Path = ROOT / "results",
               client_factory=None) -> Flask:
    """client_factory(model_alias) returns an LLM client; tests pass a fake one."""
    app = Flask(__name__)
    app.config.update(RUNS_DIR=Path(runs_dir), RESULTS_DIR=Path(results_dir), CSRF_TOKEN=secrets.token_hex(16))
    catalog = case_catalog()

    def make_client(alias: str):
        if client_factory is not None:
            return client_factory(alias)
        from src.llm import make_client as real_client
        return real_client(alias)

    def check_csrf() -> None:
        if request.form.get("csrf") != app.config["CSRF_TOKEN"]:
            abort(400, "Invalid form token. Reload the page.")

    def selected_case(case_id: str | None) -> tuple[str, dict]:
        case_id = case_id or next(iter(catalog))
        if case_id not in catalog:
            abort(404)
        return case_id, catalog[case_id]

    @app.get("/")
    def home():
        return redirect(url_for("review"))

    @app.get("/review")
    def review():
        case_id, case = selected_case(request.args.get("case"))
        runs_dir = app.config["RUNS_DIR"]
        recorded = index_runs(runs_dir, set(catalog)).get(case_id, [])
        view, label = None, None
        if recorded:
            name = request.args.get("file") or recorded[0]["file"]
            line = request.args.get("line", type=int)
            if line is None:  # first record of this case in the chosen file
                line = next((r["line"] for r in recorded if r["file"] == name), -1)
            view = record_view(load_record(runs_dir, name, line, case_id), case["row"])
            label = (f"Live run, logged to {name}" if request.args.get("live")
                     else f"Replay of recorded run {name}")
            view.update(file=name, line=line)
        return render_template(
            "review.html", tab="review", banner=BANNER, catalog=catalog, case_id=case_id, case=case,
            fields=[(f, case["row"].get(f) or "not available") for f in INPUT_FIELDS],
            recorded=recorded, view=view, label=label, versions=VERSIONS, models=sorted(config.MODELS),
            csrf=app.config["CSRF_TOKEN"], saved=request.args.get("saved"), error=request.args.get("error"),
            has_key=bool(os.environ.get("ANTHROPIC_API_KEY")) or client_factory is not None)

    @app.post("/live")
    def live():
        check_csrf()
        case_id, case = selected_case(request.form.get("case"))
        version, mode, model = request.form.get("version"), request.form.get("mode"), request.form.get("model")
        if version not in VERSIONS or mode not in (FIELDS_ONLY, WITH_MESSAGE) or model not in config.MODELS:
            abort(400, "Unknown version, mode or model.")
        if client_factory is None and not os.environ.get("ANTHROPIC_API_KEY"):
            return redirect(url_for("review", case=case_id, error="Live mode needs ANTHROPIC_API_KEY. "
                                    "Run the app from a normal terminal with the key set."))
        message = case["message"] if mode == WITH_MESSAGE else None
        run_id = f"live_{datetime.now(timezone.utc):%Y%m%d}"
        record = {"run": run_id, "repeat": 1, "source": "review_app live",
                  **run_case(case["row"], version, make_client(model), case["split"], message, case["injection"])}
        log_path = app.config["RUNS_DIR"] / f"{run_id}.jsonl"
        with log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(record) + "\n")
        line = len(log_path.read_text(encoding="utf-8").splitlines()) - 1
        return redirect(url_for("review", case=case_id, file=log_path.name, line=line, live=1))

    @app.post("/decision")
    def decision():
        check_csrf()
        case_id, case = selected_case(request.form.get("case"))
        choice = request.form.get("decision")
        if choice not in DECISIONS:
            abort(400, "Decision must be approve, edit or reject.")
        name, line = request.form.get("file", ""), request.form.get("line", type=int)
        if line is None:
            abort(400, "Missing record line.")
        record = load_record(app.config["RUNS_DIR"], name, line, case_id)
        view = record_view(record, case["row"])
        edited = request.form.get("edited_reply", "").replace("\r\n", "\n")
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "case_id": case_id, "decision": choice,
            "ai_output": {"run_log": name, "line": line, "run": record.get("run"),
                          "prompt_version": record["prompt_version"], "model": record.get("model"),
                          "mode": record["mode"], "final_route": record.get("final_route"),
                          "required_approvals": record.get("final_required_approvals"),
                          "draft_reply": view["draft"], "parsed_output": record.get("parsed_output")},
            "human_edit": edited if edited.strip() != view["draft"].strip() else None,
            "reviewer_note": request.form.get("note") or None,
        }
        with (app.config["RUNS_DIR"] / "audit.jsonl").open("a", encoding="utf-8") as audit:
            audit.write(json.dumps(entry) + "\n")
        return redirect(url_for("review", case=case_id, file=name, line=line, saved=choice))

    @app.get("/evaluation")
    def evaluation():
        results_dir = app.config["RESULTS_DIR"]
        files = sorted(p.name for p in results_dir.glob("*.md"))
        name = request.args.get("file")
        blocks = markdown_blocks(safe_file(results_dir, name, ".md").read_text(encoding="utf-8")) if name else None
        return render_template("review.html", tab="evaluation", banner=BANNER, files=files, file=name, blocks=blocks)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
