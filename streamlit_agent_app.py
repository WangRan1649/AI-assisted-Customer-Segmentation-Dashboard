from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from agents.orchestrator_agent import run_agent_request
from agents.schemas import AgentRequest


PROJECT_ROOT = Path(__file__).resolve().parent
CUSTOMER_SEGMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_segments.csv"
FACT_SCORED_PATH = PROJECT_ROOT / "data" / "processed" / "fact_user_behavior_scored.csv"
POWERBI_INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "powerbi_llm_insights.csv"
RUN_METADATA_PATH = PROJECT_ROOT / "outputs" / "run_metadata.json"
EVAL_RESULTS_PATH = PROJECT_ROOT / "eval" / "eval_results.csv"
TRACE_LOG_PATH = PROJECT_ROOT / "logs" / "agent_runs.jsonl"


def _inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #0b1f3a;
            --navy: #12365d;
            --steel: #5f6f82;
            --line: #d9dee7;
            --panel: #ffffff;
            --soft: #f6f8fb;
        }
        .stApp {
            background: #ffffff;
            color: var(--ink);
        }
        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }
        [data-testid="stSidebar"] {
            background: #f7f9fc;
            border-right: 1px solid var(--line);
        }
        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 14px 16px;
            box-shadow: 0 1px 2px rgba(10, 31, 58, 0.04);
        }
        div[data-testid="stMetric"] label {
            color: var(--steel);
            font-size: 0.82rem;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: var(--navy);
            font-size: 1.25rem;
        }
        .section-title {
            margin: 0.3rem 0 0.7rem 0;
            padding-bottom: 0.35rem;
            border-bottom: 1px solid var(--line);
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 700;
        }
        .brief-card {
            background: var(--soft);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 14px 16px;
            margin: 8px 0 14px 0;
            color: var(--ink);
        }
        .brief-card strong {
            color: var(--navy);
        }
        .small-note {
            color: var(--steel);
            font-size: 0.9rem;
            line-height: 1.55;
        }
        .stButton > button {
            border-radius: 4px;
            border: 1px solid #173b63;
            color: #0b1f3a;
            font-weight: 600;
        }
        .stButton > button[kind="primary"] {
            background: #12365d;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _run_project_command(args: list[str], timeout: int = 180) -> dict[str, Any]:
    command = [sys.executable, *args]
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return {
            "command": " ".join(args),
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "status": "success" if result.returncode == 0 else "failed",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": " ".join(args),
            "returncode": None,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "",
            "status": "timeout",
        }


def _show_command_result(result: dict[str, Any]) -> None:
    status = result.get("status")
    if status == "success":
        st.success("命令已完成。")
    elif status == "timeout":
        st.warning("命令执行超时，请检查终端或稍后重试。")
    else:
        st.error("命令执行失败。")

    st.write(f"Return code: `{result.get('returncode')}`")
    if result.get("stdout"):
        st.caption("stdout")
        st.code(result["stdout"], language="text")
    if result.get("stderr"):
        st.caption("stderr")
        st.code(result["stderr"], language="text")


def _load_csv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def _load_metadata() -> dict[str, Any] | None:
    if not RUN_METADATA_PATH.exists():
        return None
    return json.loads(RUN_METADATA_PATH.read_text(encoding="utf-8"))


def _eval_pass_rate() -> str:
    eval_results = _load_csv(EVAL_RESULTS_PATH)
    if eval_results is None or eval_results.empty:
        return "未生成"

    pass_columns = [column for column in eval_results.columns if column.endswith("_pass")]
    if not pass_columns:
        return "未生成"

    row_pass = eval_results[pass_columns].all(axis=1).mean()
    return f"{row_pass * 100:.1f}%"


def _pipeline_status() -> str:
    metadata = _load_metadata()
    if metadata is None:
        return "未运行"

    provider = metadata.get("provider", "unknown")
    fallback_used = metadata.get("fallback_used")
    validation_passed = metadata.get("validation_passed")
    if fallback_used:
        return f"{provider} / fallback"
    if validation_passed:
        return f"{provider} / 已校验"
    return f"{provider} / 待检查"


def _render_overview_cards(demo_case: str, provider: str) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("当前数据源场景", demo_case)
    col2.metric("当前 Provider", provider)
    col3.metric("Pipeline 状态", _pipeline_status())
    col4.metric("Eval Pass Rate", _eval_pass_rate())


def _render_sidebar() -> tuple[str, str]:
    st.sidebar.header("工作流控制")
    st.sidebar.markdown(
        """
        <div class="small-note">
        当前操作只会在点击按钮后执行。默认使用 <strong>mock</strong>，适合面试稳定展示；
        <strong>siliconflow</strong> 用于真实 LLM API 展示。
        </div>
        """,
        unsafe_allow_html=True,
    )
    demo_case = st.sidebar.selectbox(
        "Demo Case",
        ["baseline_original", "apparel_vip_shift"],
        index=0,
        help="选择要应用到 data/raw/ 的演示数据源场景。",
    )
    provider = st.sidebar.selectbox(
        "Provider",
        ["mock", "siliconflow"],
        index=0,
        help="mock 适合稳定展示；siliconflow 会尝试调用真实 LLM API。",
    )

    if st.sidebar.button("应用数据源场景", use_container_width=True):
        st.sidebar.write(f"正在应用数据源场景：`{demo_case}`")
        result = _run_project_command(["scripts/apply_raw_case.py", demo_case], timeout=120)
        _show_command_result(result)

    if st.sidebar.button("运行分析流水线", use_container_width=True):
        st.sidebar.write(f"正在运行分析流水线，Provider：`{provider}`")
        result = _run_project_command(["run_pipeline.py", "--provider", provider], timeout=240)
        _show_command_result(result)

    if st.sidebar.button("运行评估测试集", use_container_width=True):
        st.sidebar.write("正在运行 Eval Harness。")
        result = _run_project_command(["eval/run_eval.py"], timeout=120)
        _show_command_result(result)

    return demo_case, provider


def _render_ask_agent_tab(provider: str) -> None:
    st.markdown('<div class="section-title">业务问题输入</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="brief-card">
        这里调用现有 Router Agent / Orchestrator。默认以 dry-run 方式回答，
        不会自动切换数据源，也不会自动运行 pipeline。
        </div>
        """,
        unsafe_allow_html=True,
    )
    examples = [
        "这个数据的用户 RFM 是多少？",
        "对比 baseline_original 和 apparel_vip_shift 的分群变化",
        "如果我要切换到 apparel_vip_shift 并刷新 Power BI，需要执行什么？",
        "当前 workflow 状态如何？",
    ]
    selected_example = st.selectbox("示例问题", [""] + examples)
    question = st.text_input(
        "业务问题",
        placeholder="请输入业务问题，例如：这个数据的用户 RFM 是多少？",
    )
    effective_question = question.strip() or selected_example

    if st.button("询问 Agent", type="primary"):
        if not effective_question:
            st.warning("请输入或选择一个业务问题。")
            return

        request = AgentRequest(
            question=effective_question,
            dry_run=True,
            provider=provider,
        )
        result = run_agent_request(request)

        st.markdown('<div class="section-title">Agent 路由结果</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Intent", result.intent)
        col2.metric("Risk Level", result.risk_level)
        col3.metric("Dry Run", str(result.dry_run))
        col4.metric("Status", result.status)

        st.write("Tools")
        st.code("\n".join(result.selected_tools) or "None", language="text")

        st.markdown('<div class="section-title">Agent 回答</div>', unsafe_allow_html=True)
        st.markdown(result.final_answer)

        if result.trace_path:
            st.caption(f"Trace: {result.trace_path}")
        if result.error:
            st.error(result.error)


def _render_rfm_summary_tab() -> None:
    st.markdown('<div class="section-title">RFM 分群结果</div>', unsafe_allow_html=True)
    segments = _load_csv(CUSTOMER_SEGMENTS_PATH)
    if segments is None:
        st.warning("未找到 data/processed/customer_segments.csv。请先运行分析流水线。")
    else:
        st.dataframe(segments, use_container_width=True)

        if {"segment", "customer_count"}.issubset(segments.columns):
            st.markdown('<div class="section-title">分群人数概览</div>', unsafe_allow_html=True)
            counts = segments[["segment", "customer_count"]].copy()
            counts = counts.sort_values("customer_count", ascending=False)
            st.dataframe(counts, use_container_width=True, hide_index=True)

    fact = _load_csv(FACT_SCORED_PATH)
    if fact is None:
        st.warning("未找到 data/processed/fact_user_behavior_scored.csv。请先运行分析流水线。")
    elif "segment_name_cn" not in fact.columns:
        st.warning("fact_user_behavior_scored.csv 中缺少 segment_name_cn 字段。")
    else:
        st.markdown('<div class="section-title">中文分群分布</div>', unsafe_allow_html=True)
        cn_counts = (
            fact["segment_name_cn"]
            .value_counts()
            .rename_axis("segment_name_cn")
            .reset_index(name="user_count")
        )
        st.dataframe(cn_counts, use_container_width=True, hide_index=True)


def _render_powerbi_outputs_tab() -> None:
    st.markdown('<div class="section-title">Power BI AI Insight Box 输出</div>', unsafe_allow_html=True)
    insights = _load_csv(POWERBI_INSIGHTS_PATH)
    if insights is None:
        st.warning("未找到 outputs/powerbi_llm_insights.csv。请先运行分析流水线。")
    else:
        st.dataframe(insights, use_container_width=True)

    metadata = _load_metadata()
    if metadata is None:
        st.warning("未找到 outputs/run_metadata.json。请先运行分析流水线。")
    else:
        st.markdown('<div class="section-title">Run Metadata 摘要</div>', unsafe_allow_html=True)
        summary_keys = [
            "run_time_utc",
            "requested_provider",
            "provider",
            "model",
            "api_reached",
            "validation_passed",
            "fallback_used",
            "retry_count",
            "error_type",
            "raw_row_count",
            "processed_customer_count",
        ]
        summary = {key: metadata.get(key) for key in summary_keys}
        st.json(summary)

    st.info("Power BI 刷新后会读取这些输出文件。主图表读取 scored fact 表，AI Insight Box 读取 insight CSV。")


def _eval_summary(eval_results: pd.DataFrame) -> pd.DataFrame:
    pass_columns = [column for column in eval_results.columns if column.endswith("_pass")]
    rows = []
    for column in pass_columns:
        rows.append(
            {
                "metric": column,
                "pass_rate": round(float(eval_results[column].mean()) * 100, 1),
                "passed": int(eval_results[column].sum()),
                "total": len(eval_results),
            }
        )
    return pd.DataFrame(rows)


def _read_recent_traces(limit: int = 5) -> list[dict[str, Any]]:
    if not TRACE_LOG_PATH.exists():
        return []

    lines = TRACE_LOG_PATH.read_text(encoding="utf-8").splitlines()
    recent_lines = [line for line in lines if line.strip()][-limit:]
    traces: list[dict[str, Any]] = []
    for line in recent_lines:
        try:
            traces.append(json.loads(line))
        except json.JSONDecodeError:
            traces.append({"raw": line})
    return traces


def _render_eval_trace_tab() -> None:
    st.markdown('<div class="section-title">Eval Harness 结果</div>', unsafe_allow_html=True)
    eval_results = _load_csv(EVAL_RESULTS_PATH)
    if eval_results is None:
        st.warning("未找到 eval/eval_results.csv。请先运行评估测试集。")
    else:
        st.dataframe(eval_results, use_container_width=True)
        st.markdown('<div class="section-title">Eval Summary</div>', unsafe_allow_html=True)
        st.dataframe(_eval_summary(eval_results), use_container_width=True, hide_index=True)

    traces = _read_recent_traces()
    st.markdown('<div class="section-title">最近 5 条 Trace</div>', unsafe_allow_html=True)
    if not traces:
        st.caption("当前未发现 logs/agent_runs.jsonl。")
    else:
        st.json(traces)


def main() -> None:
    st.set_page_config(page_title="AI BI 智能分析工作台", layout="wide")
    _inject_css()

    st.title("AI BI 智能分析工作台")
    st.caption("面向业务人员的 AI 辅助商业智能分析流程")

    demo_case, provider = _render_sidebar()
    _render_overview_cards(demo_case, provider)

    st.markdown(
        """
        <div class="brief-card">
        本页面面向 HR / 面试官展示：业务解释以中文呈现，配置项、命令、Provider、
        Intent、Tools、Risk Level、Dry Run、Trace 等系统字段保留英文，便于说明工程边界。
        </div>
        """,
        unsafe_allow_html=True,
    )

    ask_tab, rfm_tab, powerbi_tab, eval_trace_tab = st.tabs(
        ["业务问答", "RFM 分群概览", "Power BI 输出", "评估与 Trace"]
    )

    with ask_tab:
        _render_ask_agent_tab(provider)
    with rfm_tab:
        _render_rfm_summary_tab()
    with powerbi_tab:
        _render_powerbi_outputs_tab()
    with eval_trace_tab:
        _render_eval_trace_tab()


if __name__ == "__main__":
    main()
