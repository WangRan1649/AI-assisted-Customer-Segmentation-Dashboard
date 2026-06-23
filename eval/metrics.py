from __future__ import annotations

from typing import Any


PASS_FIELDS = [
    "intent_pass",
    "tools_pass",
    "risk_pass",
    "dry_run_pass",
    "refusal_pass",
    "contains_pass",
]


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def _accuracy(rows: list[dict[str, Any]], field: str) -> float:
    if not rows:
        return 0.0
    passed = sum(1 for row in rows if _as_bool(row.get(field)))
    return passed / len(rows)


def intent_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "intent_pass")


def tool_selection_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "tools_pass")


def risk_level_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "risk_pass")


def dry_run_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "dry_run_pass")


def refusal_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "refusal_pass")


def answer_contains_accuracy(rows: list[dict[str, Any]]) -> float:
    return _accuracy(rows, "contains_pass")


def overall_pass_rate(rows: list[dict[str, Any]]) -> float:
    if not rows:
        return 0.0

    passed = 0
    for row in rows:
        if all(_as_bool(row.get(field)) for field in PASS_FIELDS):
            passed += 1

    return passed / len(rows)


def format_percentage(value: float) -> str:
    return f"{value * 100:.1f}%"
