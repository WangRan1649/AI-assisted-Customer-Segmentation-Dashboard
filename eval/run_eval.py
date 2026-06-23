from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.orchestrator_agent import run_agent_request  # noqa: E402
from agents.schemas import AgentRequest  # noqa: E402
from eval.metrics import (  # noqa: E402
    answer_contains_accuracy,
    dry_run_accuracy,
    format_percentage,
    intent_accuracy,
    overall_pass_rate,
    refusal_accuracy,
    risk_level_accuracy,
    tool_selection_accuracy,
)


DATASET_PATH = PROJECT_ROOT / "eval" / "eval_dataset.csv"
RESULTS_PATH = PROJECT_ROOT / "eval" / "eval_results.csv"

RESULT_FIELDS = [
    "id",
    "question",
    "expected_intent",
    "actual_intent",
    "intent_pass",
    "expected_tools",
    "actual_tools",
    "tools_pass",
    "expected_risk_level",
    "actual_risk_level",
    "risk_pass",
    "expected_dry_run",
    "actual_dry_run",
    "dry_run_pass",
    "expected_refusal",
    "actual_refusal",
    "refusal_pass",
    "expected_contains",
    "contains_pass",
    "final_answer_preview",
]


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def split_pipe(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in value.split("|") if item.strip()]


def normalize_tools(tools: list[str]) -> list[str]:
    return sorted(tool.strip() for tool in tools if tool.strip())


def answer_contains(final_answer: str, expected_contains: list[str]) -> bool:
    return all(token in final_answer for token in expected_contains)


def preview(text: str, max_length: int = 220) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 3] + "..."


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    request = AgentRequest(
        question=row["question"],
        dry_run=True,
        provider="mock",
        trace_enabled=False,
    )
    result = run_agent_request(request)

    expected_tools = normalize_tools(split_pipe(row["expected_tools"]))
    actual_tools = normalize_tools(result.selected_tools)
    expected_contains = split_pipe(row["expected_contains"])
    expected_refusal = parse_bool(row["expected_refusal"])

    actual_refusal = result.status == "refused"

    return {
        "id": row["id"],
        "question": row["question"],
        "expected_intent": row["expected_intent"],
        "actual_intent": result.intent,
        "intent_pass": result.intent == row["expected_intent"],
        "expected_tools": "|".join(expected_tools),
        "actual_tools": "|".join(actual_tools),
        "tools_pass": expected_tools == actual_tools,
        "expected_risk_level": row["expected_risk_level"],
        "actual_risk_level": result.risk_level,
        "risk_pass": result.risk_level == row["expected_risk_level"],
        "expected_dry_run": row["expected_dry_run"],
        "actual_dry_run": result.dry_run,
        "dry_run_pass": result.dry_run == parse_bool(row["expected_dry_run"]),
        "expected_refusal": row["expected_refusal"],
        "actual_refusal": actual_refusal,
        "refusal_pass": actual_refusal == expected_refusal,
        "expected_contains": row["expected_contains"],
        "contains_pass": answer_contains(result.final_answer, expected_contains),
        "final_answer_preview": preview(result.final_answer),
    }


def read_dataset() -> list[dict[str, str]]:
    with DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as dataset_file:
        return list(csv.DictReader(dataset_file))


def write_results(rows: list[dict[str, Any]]) -> None:
    with RESULTS_PATH.open("w", encoding="utf-8-sig", newline="") as results_file:
        writer = csv.DictWriter(results_file, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    dataset = read_dataset()
    results = [evaluate_row(row) for row in dataset]
    write_results(results)

    print(f"Total cases: {len(results)}")
    print(f"Intent accuracy: {format_percentage(intent_accuracy(results))}")
    print(f"Tool selection accuracy: {format_percentage(tool_selection_accuracy(results))}")
    print(f"Risk level accuracy: {format_percentage(risk_level_accuracy(results))}")
    print(f"Dry-run accuracy: {format_percentage(dry_run_accuracy(results))}")
    print(f"Refusal accuracy: {format_percentage(refusal_accuracy(results))}")
    print(f"Answer contains accuracy: {format_percentage(answer_contains_accuracy(results))}")
    print(f"Overall pass rate: {format_percentage(overall_pass_rate(results))}")
    print(f"Results saved to: eval/eval_results.csv")


if __name__ == "__main__":
    main()
