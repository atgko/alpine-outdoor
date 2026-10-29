"""Create the tune and holdout splits, stratified by assigned_owner.

Run once:  python -m eval.split
Writes eval/splits/tune.txt and eval/splits/holdout.txt (one case id per line).
The holdout set is locked: use it only for final configurations.
"""
from __future__ import annotations

import csv
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES_CSV = ROOT / "data" / "Alpine_Outdoor_Customer_Support_Case_Data.csv"
SPLITS_DIR = ROOT / "eval" / "splits"
SEED = 6490
HOLDOUT_SIZE = 20


def load_cases(path: Path = CASES_CSV) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def holdout_quotas(group_sizes: dict[str, int], holdout_size: int) -> dict[str, int]:
    """Proportional quotas per group, rounded with the largest remainder method."""
    total = sum(group_sizes.values())
    exact = {g: n * holdout_size / total for g, n in group_sizes.items()}
    quotas = {g: math.floor(x) for g, x in exact.items()}
    by_remainder = sorted(exact, key=lambda g: (-(exact[g] - quotas[g]), g))
    for g in by_remainder[: holdout_size - sum(quotas.values())]:
        quotas[g] += 1
    return quotas


def make_split(cases: list[dict[str, str]], seed: int = SEED,
               holdout_size: int = HOLDOUT_SIZE) -> tuple[list[str], list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for case in cases:
        groups[case["assigned_owner"]].append(case["case_id"])
    quotas = holdout_quotas({g: len(ids) for g, ids in groups.items()}, holdout_size)
    rng = random.Random(seed)
    holdout: list[str] = []
    for group in sorted(groups):
        holdout += rng.sample(sorted(groups[group]), quotas[group])
    held = set(holdout)
    tune = sorted(c["case_id"] for c in cases if c["case_id"] not in held)
    return tune, sorted(holdout)


def load_split(name: str) -> list[str]:
    return (SPLITS_DIR / f"{name}.txt").read_text(encoding="utf-8").split()


def main() -> None:
    tune, holdout = make_split(load_cases())
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    (SPLITS_DIR / "tune.txt").write_text("\n".join(tune) + "\n", encoding="utf-8")
    (SPLITS_DIR / "holdout.txt").write_text("\n".join(holdout) + "\n", encoding="utf-8")
    print(f"seed={SEED} tune={len(tune)} holdout={len(holdout)}")


if __name__ == "__main__":
    main()
