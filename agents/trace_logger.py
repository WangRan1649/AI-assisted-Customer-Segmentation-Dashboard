from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from agents import PROJECT_ROOT
from agents.schemas import AgentPlan, AgentResult


TRACE_PATH = PROJECT_ROOT / "logs" / "agent_runs.jsonl"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def log_agent_run(plan: AgentPlan, result: AgentResult) -> str:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid4())
    record: dict[str, Any] = {
        "run_id": run_id,
        "timestamp": utc_now_iso(),
        "question": plan.question,
        "intent": plan.intent,
        "selected_tools": plan.selected_tools,
        "dry_run": plan.dry_run,
        "status": result.status,
        "error": result.error,
        "risk_level": plan.risk_level,
        "requires_execution": plan.requires_execution,
    }

    with TRACE_PATH.open("a", encoding="utf-8") as trace_file:
        trace_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return str(TRACE_PATH.relative_to(PROJECT_ROOT)).replace("\\", "/")


def result_to_dict(result: AgentResult) -> dict[str, Any]:
    return asdict(result)
