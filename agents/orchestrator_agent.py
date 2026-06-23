from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd

from agents import PROJECT_ROOT
from agents.schemas import AgentPlan, AgentRequest, AgentResult, AgentStep
from agents.trace_logger import log_agent_run
from agents.router_agent import route_request


DEMO_CASES_DIR = PROJECT_ROOT / "data" / "demo_cases"
RUN_METADATA_PATH = PROJECT_ROOT / "outputs" / "run_metadata.json"
CUSTOMER_SEGMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_segments.csv"
APPLY_RAW_CASE_SCRIPT = PROJECT_ROOT / "scripts" / "apply_raw_case.py"
RUN_PIPELINE_SCRIPT = PROJECT_ROOT / "run_pipeline.py"
ALLOWED_CASES = {"baseline_original", "apparel_vip_shift"}

SEGMENT_CN = {
    "High-value Customers": "高价值用户",
    "Potential Customers": "潜力用户",
    "Churn-risk Customers": "流失风险用户",
    "Regular Retained Customers": "一般保持用户",
    "Other Customers": "其他用户",
}

SEGMENT_INTERPRETATION_CN = {
    "High-value Customers": "核心利润来源，应优先做会员权益、忠诚度保护和高价值品类推荐。",
    "Potential Customers": "用户基数较大，但复购频次偏低，适合用复购激励和组合推荐推动转化。",
    "Churn-risk Customers": "历史消费能力较强但近期活跃不足，应通过召回、服务跟进和品类提醒恢复关系。",
    "Regular Retained Customers": "购买习惯相对稳定但客单价值较低，适合做追加销售和使用场景拓展。",
    "Other Customers": "短期价值和互动程度较低，建议用低成本触达进行长期培育。",
}


def _relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def _ensure_project_path(path: Path) -> Path:
    resolved = path.resolve()
    project_root = PROJECT_ROOT.resolve()
    if resolved != project_root and project_root not in resolved.parents:
        raise ValueError(f"Path is outside project root: {path}")
    return resolved


def _detect_case_name(question: str) -> str:
    normalized = question.lower()
    for case_name in sorted(ALLOWED_CASES):
        if case_name.lower() in normalized:
            return case_name
    return "apparel_vip_shift"


def _list_demo_cases() -> tuple[str, dict[str, Any]]:
    _ensure_project_path(DEMO_CASES_DIR)
    cases = []
    if DEMO_CASES_DIR.exists():
        for case_dir in sorted(DEMO_CASES_DIR.iterdir()):
            if case_dir.is_dir() and (case_dir / "raw.csv").exists():
                cases.append(case_dir.name)

    answer = "可用数据场景：\n" + "\n".join(f"- {case}" for case in cases)
    return answer, {"cases": cases}


def _compare_demo_cases() -> tuple[str, dict[str, Any]]:
    baseline_path = _ensure_project_path(DEMO_CASES_DIR / "baseline_original" / "customer_segments.csv")
    apparel_path = _ensure_project_path(DEMO_CASES_DIR / "apparel_vip_shift" / "customer_segments.csv")

    baseline = pd.read_csv(baseline_path)
    apparel = pd.read_csv(apparel_path)

    merged = baseline[["segment", "customer_count", "share", "weighted_aov"]].merge(
        apparel[["segment", "customer_count", "share", "weighted_aov"]],
        on="segment",
        suffixes=("_baseline", "_apparel_shift"),
    )
    merged["customer_count_delta"] = (
        merged["customer_count_apparel_shift"] - merged["customer_count_baseline"]
    )
    merged["weighted_aov_delta"] = (
        merged["weighted_aov_apparel_shift"] - merged["weighted_aov_baseline"]
    ).round(2)

    lines = [
        "分群对比：baseline_original -> apparel_vip_shift",
        "",
        "| Segment | Baseline customers | Apparel shift customers | Customer delta | Baseline AOV | Apparel shift AOV | AOV delta |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in merged.to_dict(orient="records"):
        lines.append(
            "| {segment} | {customer_count_baseline} | {customer_count_apparel_shift} | "
            "{customer_count_delta:+d} | {weighted_aov_baseline:.2f} | "
            "{weighted_aov_apparel_shift:.2f} | {weighted_aov_delta:+.2f} |".format(
                **row
            )
        )

    lines.extend(["", "业务解读："])
    for row in merged.to_dict(orient="records"):
        delta = int(row["customer_count_delta"])
        if delta > 0:
            change_text = f"增加 {delta} 人"
        elif delta < 0:
            change_text = f"减少 {abs(delta)} 人"
        else:
            change_text = "保持不变"
        segment = row["segment"]
        lines.append(
            "- {segment}（{segment_cn}）：{baseline} -> {shift}，{change_text}；"
            "Weighted AOV 从 {baseline_aov:.2f} 变为 {shift_aov:.2f}，AOV 变化 {aov_delta:+.2f}。".format(
                segment=segment,
                segment_cn=SEGMENT_CN.get(segment, segment),
                baseline=int(row["customer_count_baseline"]),
                shift=int(row["customer_count_apparel_shift"]),
                change_text=change_text,
                baseline_aov=float(row["weighted_aov_baseline"]),
                shift_aov=float(row["weighted_aov_apparel_shift"]),
                aov_delta=float(row["weighted_aov_delta"]),
            )
        )

    return "\n".join(lines), {"comparison": merged.to_dict(orient="records")}


def _workflow_status() -> tuple[str, dict[str, Any]]:
    metadata_path = _ensure_project_path(RUN_METADATA_PATH)
    if not metadata_path.exists():
        return "未找到 outputs/run_metadata.json。请先运行 pipeline 生成 workflow metadata。", {}

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    answer = "\n".join(
        [
            "当前 workflow 状态：",
            f"- run_time_utc: {metadata.get('run_time_utc')}",
            f"- requested_provider: {metadata.get('requested_provider')}",
            f"- provider: {metadata.get('provider')}",
            f"- model: {metadata.get('model')}",
            f"- api_reached: {metadata.get('api_reached')}",
            f"- validation_passed: {metadata.get('validation_passed')}",
            f"- fallback_used: {metadata.get('fallback_used')}",
            f"- retry_count: {metadata.get('retry_count')}",
            f"- error_type: {metadata.get('error_type')}",
            f"- raw_row_count: {metadata.get('raw_row_count')}",
            f"- processed_customer_count: {metadata.get('processed_customer_count')}",
            "",
            "业务含义：如果 provider 为 mock，说明当前结果适合稳定演示；如果 provider 为 siliconflow 且 "
            "api_reached=True、validation_passed=True、fallback_used=False，说明已真实调用 API 并通过数字校验。",
        ]
    )

    return answer, {"metadata": metadata}


def _rfm_summary_question() -> tuple[str, dict[str, Any]]:
    segment_path = _ensure_project_path(CUSTOMER_SEGMENTS_PATH)
    if not segment_path.exists():
        return "未找到 data/processed/customer_segments.csv。请先运行分析流水线。", {}

    segments = pd.read_csv(segment_path)
    required_columns = [
        "segment",
        "customer_count",
        "share",
        "weighted_aov",
        "avg_rfm_score",
        "business_role",
        "action_priority",
    ]
    missing_columns = [column for column in required_columns if column not in segments.columns]
    if missing_columns:
        raise ValueError(
            "customer_segments.csv is missing required columns: "
            + ", ".join(missing_columns)
        )

    total_customers = int(segments["customer_count"].sum())
    lines = [
        "RFM 分群摘要（来源：data/processed/customer_segments.csv）",
        "",
        f"当前数据共 {total_customers} 个用户。",
        "",
        "| Segment | 中文分群 | Customers | Share | Weighted AOV | Avg RFM Score | 业务解释 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in segments[required_columns].to_dict(orient="records"):
        segment = row["segment"]
        lines.append(
            "| {segment} | {segment_cn} | {customer_count} | {share} | {weighted_aov:.2f} | "
            "{avg_rfm_score:.2f} | {interpretation} |".format(
                segment=segment,
                segment_cn=SEGMENT_CN.get(segment, segment),
                customer_count=int(row["customer_count"]),
                share=row["share"],
                weighted_aov=float(row["weighted_aov"]),
                avg_rfm_score=float(row["avg_rfm_score"]),
                interpretation=SEGMENT_INTERPRETATION_CN.get(segment, "需要业务人员进一步复核。"),
            )
        )

    lines.extend(
        [
            "",
            "管理建议：",
            "- 先保护高价值用户，再对潜力用户做转化，避免只看用户数而忽略价值差异。",
            "- 对流失风险用户建议使用召回和服务跟进，不宜直接归为低价值用户。",
            "- 一般保持用户适合做品类扩展和追加销售，其他用户适合低成本培育。",
            "",
            "以上数字均直接读取自 Python 生成的 CSV，没有使用 LLM 计算数字。",
        ]
    )

    return "\n".join(lines), {"segments": segments[required_columns].to_dict(orient="records")}


def _explain_powerbi_workflow() -> tuple[str, dict[str, Any]]:
    answer = "\n".join(
        [
            "Power BI 工作流：",
            "- 主图表建议读取 data/processed/fact_user_behavior_scored.csv。",
            "- AI Insight Box 读取 outputs/powerbi_llm_insights.csv。",
            "- 这两个文件来自同一次 V3 pipeline，因此分群人数和 AI 洞察应保持一致。",
            "- 如果主图表和 AI Insight Box 的人数不一致，通常是 Power BI 仍连接旧表或旧分群字段。",
            "- 运行 workflow 后，打开 PBIX 文件并点击 Home -> Refresh。",
        ]
    )
    return answer, {}


def _run_workflow(plan: AgentPlan, request: AgentRequest) -> tuple[str, dict[str, Any]]:
    case_name = _detect_case_name(plan.question)
    commands = [
        f".venv\\Scripts\\python.exe scripts\\apply_raw_case.py {case_name}",
        ".venv\\Scripts\\python.exe run_pipeline.py --provider mock",
    ]

    if plan.dry_run:
        answer = "\n".join(
            [
                "当前为 dry-run，不会修改文件，也不会运行 pipeline。",
                "如需真正执行，请使用 --execute，或在 Streamlit sidebar 中点击对应按钮。",
                "计划执行命令：",
                *[f"- {command}" for command in commands],
                "随后在 Power BI 中执行：Home -> Refresh。",
            ]
        )
        return answer, {"case_name": case_name, "commands": commands, "executed": False}

    if request.provider != "mock":
        raise ValueError("Execution mode only allows run_pipeline.py --provider mock in V3.3.")

    apply_script = _ensure_project_path(APPLY_RAW_CASE_SCRIPT)
    pipeline_script = _ensure_project_path(RUN_PIPELINE_SCRIPT)

    apply_result = subprocess.run(
        [sys.executable, str(apply_script), case_name],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    pipeline_result = subprocess.run(
        [sys.executable, str(pipeline_script), "--provider", "mock"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    answer = "\n".join(
        [
            f"已切换 demo 数据场景并运行 mock workflow：{case_name}。",
            "下一步请在 Power BI 中执行：Home -> Refresh。",
        ]
    )
    return answer, {
        "case_name": case_name,
        "commands": commands,
        "executed": True,
        "apply_raw_case_stdout": apply_result.stdout,
        "pipeline_stdout": pipeline_result.stdout,
    }


def _apply_step_outputs(plan: AgentPlan, output: dict[str, Any]) -> list[AgentStep]:
    steps = []
    for step in plan.steps:
        step.status = "completed"
        step.output = output
        steps.append(step)
    return steps


def _attach_trace_if_enabled(
    request: AgentRequest,
    plan: AgentPlan,
    result: AgentResult,
) -> AgentResult:
    if request.trace_enabled:
        result.trace_path = log_agent_run(plan, result)
    return result


def run_agent_request(request: AgentRequest) -> AgentResult:
    plan = route_request(request)

    if plan.refusal_reason:
        result = AgentResult(
            question=plan.question,
            intent=plan.intent,
            selected_tools=plan.selected_tools,
            risk_level=plan.risk_level,
            requires_execution=plan.requires_execution,
            dry_run=plan.dry_run,
            final_answer=plan.refusal_reason,
            status="refused",
            error=plan.refusal_reason,
            steps=plan.steps,
        )
        return _attach_trace_if_enabled(request, plan, result)

    try:
        if plan.intent == "list_demo_cases":
            final_answer, output = _list_demo_cases()
        elif plan.intent == "compare_demo_cases":
            final_answer, output = _compare_demo_cases()
        elif plan.intent == "workflow_status":
            final_answer, output = _workflow_status()
        elif plan.intent == "rfm_summary_question":
            final_answer, output = _rfm_summary_question()
        elif plan.intent == "run_workflow":
            final_answer, output = _run_workflow(plan, request)
        elif plan.intent == "explain_powerbi_workflow":
            final_answer, output = _explain_powerbi_workflow()
        else:
            final_answer = (
                "无法识别这个请求。你可以尝试询问：列出可用数据场景、对比 demo case、"
                "查看 workflow 状态、解释 Power BI 工作流，或 dry-run 一个数据切换流程。"
            )
            output = {}

        result = AgentResult(
            question=plan.question,
            intent=plan.intent,
            selected_tools=plan.selected_tools,
            risk_level=plan.risk_level,
            requires_execution=plan.requires_execution,
            dry_run=plan.dry_run,
            final_answer=final_answer,
            status="ok",
            steps=_apply_step_outputs(plan, output),
        )
    except Exception as exc:
        result = AgentResult(
            question=plan.question,
            intent=plan.intent,
            selected_tools=plan.selected_tools,
            risk_level=plan.risk_level,
            requires_execution=plan.requires_execution,
            dry_run=plan.dry_run,
            final_answer=f"Agent 运行失败：{exc}",
            status="error",
            error=str(exc),
            steps=plan.steps,
        )

    return _attach_trace_if_enabled(request, plan, result)
