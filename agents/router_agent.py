from __future__ import annotations

from agents.schemas import AgentPlan, AgentRequest, AgentStep


HIGH_RISK_KEYWORDS = [
    "delete",
    "remove",
    "clear",
    "reset",
    "drop",
    "overwrite",
    "purge",
    "删除",
    "清空",
    "重置",
    "覆盖",
]


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _build_steps(intent: str) -> list[AgentStep]:
    if intent == "list_demo_cases":
        return [
            AgentStep(
                name="List demo cases",
                tool="filesystem:data/demo_cases",
                description="Read demo case folders under data/demo_cases.",
            )
        ]

    if intent == "compare_demo_cases":
        return [
            AgentStep(
                name="Read baseline segments",
                tool="pandas:data/demo_cases/baseline_original/customer_segments.csv",
                description="Load baseline customer segment summary.",
            ),
            AgentStep(
                name="Read apparel shift segments",
                tool="pandas:data/demo_cases/apparel_vip_shift/customer_segments.csv",
                description="Load apparel_vip_shift customer segment summary.",
            ),
            AgentStep(
                name="Compare segment counts",
                tool="python:pandas",
                description="Compare segment counts, shares, weighted AOV, and action priority.",
            ),
        ]

    if intent == "workflow_status":
        return [
            AgentStep(
                name="Read workflow metadata",
                tool="json:outputs/run_metadata.json",
                description="Summarize latest pipeline provider, validation, fallback, and output files.",
            )
        ]

    if intent == "rfm_summary_question":
        return [
            AgentStep(
                name="Read customer segment summary",
                tool="pandas:data/processed/customer_segments.csv",
                description="Read Python-computed segment counts, shares, weighted AOV, and RFM scores.",
            ),
            AgentStep(
                name="Explain RFM summary",
                tool="python:pandas",
                description="Summarize RFM segment results without calling an LLM.",
            ),
        ]

    if intent == "run_workflow":
        return [
            AgentStep(
                name="Switch raw demo case",
                tool="scripts/apply_raw_case.py",
                description="Apply a whitelisted demo raw case when execution is explicitly enabled.",
            ),
            AgentStep(
                name="Run BI workflow",
                tool="run_pipeline.py --provider mock",
                description="Run the existing mock workflow when execution is explicitly enabled.",
            ),
        ]

    if intent == "explain_powerbi_workflow":
        return [
            AgentStep(
                name="Explain Power BI workflow",
                tool="docs/runtime",
                description="Explain how scored fact CSV and AI insight CSV connect to Power BI refresh.",
            )
        ]

    return [
        AgentStep(
            name="No matching route",
            tool="router_agent",
            description="Ask for a clearer workflow, demo case, status, or Power BI question.",
        )
    ]


def route_request(request: AgentRequest) -> AgentPlan:
    question = request.question.strip()
    normalized = question.lower()

    if _contains_any(normalized, HIGH_RISK_KEYWORDS):
        return AgentPlan(
            question=question,
            intent="unknown",
            selected_tools=[],
            risk_level="high",
            requires_execution=False,
            dry_run=True,
            refusal_reason=(
                "检测到高风险文件操作。当前轻量 Agent 不会删除、清空、重置或覆盖非 raw 数据文件。"
            ),
        )

    if _contains_any(normalized, ["切换", "运行 workflow", "run workflow", "刷新 power bi", "apply_raw_case"]):
        intent = "run_workflow"
    elif _contains_any(normalized, ["rfm", "用户 rfm", "rfm 是多少", "rfm是多少", "客户分群结果", "用户分群结果"]):
        intent = "rfm_summary_question"
    elif _contains_any(normalized, ["列出", "可用", "list", "demo cases", "数据场景", "场景"]):
        intent = "list_demo_cases"
    elif _contains_any(normalized, ["对比", "compare", "变化", "baseline", "apparel_vip_shift"]):
        intent = "compare_demo_cases"
    elif _contains_any(normalized, ["状态", "status", "metadata", "run_metadata", "当前 workflow"]):
        intent = "workflow_status"
    elif _contains_any(normalized, ["power bi", "powerbi", "主图表", "insight box", "联动", "自动化流程"]):
        intent = "explain_powerbi_workflow"
    else:
        intent = "unknown"

    requires_execution = intent == "run_workflow"
    risk_level = "medium" if requires_execution else "low"
    steps = _build_steps(intent)

    return AgentPlan(
        question=question,
        intent=intent,
        selected_tools=[step.tool for step in steps],
        risk_level=risk_level,
        requires_execution=requires_execution,
        dry_run=request.dry_run,
        steps=steps,
    )
