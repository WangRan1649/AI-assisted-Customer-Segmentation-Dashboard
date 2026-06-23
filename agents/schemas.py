from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRequest:
    question: str
    dry_run: bool = True
    provider: str = "mock"


@dataclass
class AgentStep:
    name: str
    tool: str
    description: str
    status: str = "planned"
    output: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentPlan:
    question: str
    intent: str
    selected_tools: list[str]
    risk_level: str
    requires_execution: bool
    dry_run: bool
    steps: list[AgentStep] = field(default_factory=list)
    refusal_reason: str | None = None


@dataclass
class AgentResult:
    question: str
    intent: str
    selected_tools: list[str]
    risk_level: str
    requires_execution: bool
    dry_run: bool
    final_answer: str
    status: str = "ok"
    error: str | None = None
    trace_path: str | None = None
    steps: list[AgentStep] = field(default_factory=list)
