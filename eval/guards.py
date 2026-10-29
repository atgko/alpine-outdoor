"""Run guards shared by every evaluation script: holdout lock and spend guard."""
from __future__ import annotations

from eval.split import load_split
from src import config


class GuardError(RuntimeError):
    pass


def split_of(case_ids: list[str]) -> dict[str, str]:
    tune, holdout = set(load_split("tune")), set(load_split("holdout"))
    return {c: "holdout" if c in holdout else "tune" if c in tune else "other" for c in case_ids}


def check_holdout(case_ids: list[str], holdout: bool, final: bool) -> list[str]:
    """Refuse holdout cases unless both --holdout and --final are given.
    Returns warning lines to write into the run log."""
    touched = [c for c, s in split_of(case_ids).items() if s == "holdout"]
    if touched and not (holdout and final):
        raise GuardError(f"{len(touched)} holdout case(s) requested ({', '.join(touched)}). "
                         "The holdout is locked. Use --holdout --final only for final configurations.")
    return [f"HOLDOUT TOUCHED: {', '.join(touched)}"] if touched else []


def estimate_calls(n_cases: int, versions: list[str], n_modes: int, repeats: int = 1) -> tuple[int, int]:
    """(expected calls, upper bound if every v2 to v4 call needs its one schema retry)."""
    base = n_cases * len(versions) * n_modes * repeats
    retries = n_cases * sum(v != "v1" for v in versions) * n_modes * repeats
    return base, base + retries


def check_spend(expected: int, upper: int, yes: bool) -> None:
    """The guard uses the upper bound, so retries cannot push a run past the limit unseen."""
    print(f"Estimated API calls: {expected} (up to {upper} if every schema retry is used)")
    if upper > config.CONFIRM_ABOVE_CALLS and not yes:
        raise GuardError(f"Run exceeds {config.CONFIRM_ABOVE_CALLS} calls. Re-run with --yes to proceed.")
