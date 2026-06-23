from __future__ import annotations

import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

try:
    import altair as alt
except ModuleNotFoundError:  # pragma: no cover - runtime fallback for lean envs
    alt = None

from agents.orchestrator_agent import run_agent_request
from agents.schemas import AgentRequest, AgentResult


PROJECT_ROOT = Path(__file__).resolve().parent
CUSTOMER_SEGMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_segments.csv"
FACT_SCORED_PATH = PROJECT_ROOT / "data" / "processed" / "fact_user_behavior_scored.csv"
POWERBI_INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "powerbi_llm_insights.csv"
RUN_METADATA_PATH = PROJECT_ROOT / "outputs" / "run_metadata.json"
EVAL_RESULTS_PATH = PROJECT_ROOT / "eval" / "eval_results.csv"
TRACE_LOG_PATH = PROJECT_ROOT / "logs" / "agent_runs.jsonl"

SEGMENT_CN = {
    "High-value Customers": "高价值用户",
    "Potential Customers": "潜力用户",
    "Churn-risk Customers": "流失风险用户",
    "Regular Retained Customers": "一般保持用户",
    "Other Customers": "其他用户",
}

NAVY = "#12365D"
INK = "#0B1F3A"
STEEL = "#5F6F82"
LINE = "#D9DEE7"
LIGHT = "#F6F8FB"
BAR = "#2E5E8C"
BAR_2 = "#6F879F"
PALETTE = ["#12365D", "#2E5E8C", "#6F879F", "#9BAABD", "#D9DEE7"]


def _inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #0b1f3a;
            --navy: #12365d;
            --steel: #5f6f82;
            --line: #d9dee7;
            --light: #f6f8fb;
            --panel: #ffffff;
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
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
        }
        .hero {
            border-bottom: 1px solid var(--line);
            padding: 0.25rem 0 1.25rem 0;
            margin-bottom: 1.1rem;
        }
        .hero h1 {
            font-size: 2.2rem;
            line-height: 1.18;
            margin: 0 0 0.45rem 0;
            font-weight: 760;
        }
        .hero p {
            color: var(--steel);
            font-size: 1rem;
            margin: 0;
        }
        .section-title {
            margin: 1.2rem 0 0.75rem 0;
            padding-bottom: 0.45rem;
            border-bottom: 1px solid var(--line);
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 720;
        }
        .section-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 16px 18px;
            margin: 0.5rem 0 1rem 0;
        }
        .metric-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 14px 16px;
            min-height: 92px;
            box-shadow: 0 1px 2px rgba(10, 31, 58, 0.04);
        }
        .metric-label {
            color: var(--steel);
            font-size: 0.8rem;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            color: var(--navy);
            font-size: 1.35rem;
            font-weight: 760;
            line-height: 1.2;
        }
        .metric-sub {
            color: var(--steel);
            font-size: 0.78rem;
            margin-top: 0.35rem;
        }
        .insight-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 4px solid var(--navy);
            border-radius: 6px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }
        .insight-title {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 720;
            margin-bottom: 0.35rem;
        }
        .insight-meta {
            color: var(--steel);
            font-size: 0.82rem;
            margin-bottom: 0.55rem;
        }
        .insight-body {
            color: var(--ink);
            font-size: 0.92rem;
            line-height: 1.65;
        }
        .muted {
            color: var(--steel);
            font-size: 0.82rem;
        }
        .answer-card {
            background: var(--light);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 16px 18px;
            margin-top: 0.9rem;
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
            font-size: 1.28rem;
        }
        .stButton > button {
            border-radius: 4px;
            border: 1px solid #173b63;
            color: #0b1f3a;
            font-weight: 650;
        }
        .stButton > button[kind="primary"] {
            background: #12365d;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _load_csv(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def _load_metadata() -> dict[str, Any] | None:
    if not RUN_METADATA_PATH.exists():
        return None
    return json.loads(RUN_METADATA_PATH.read_text(encoding="utf-8"))


def _find_column(df: pd.DataFrame | None, candidates: list[str]) -> str | None:
    if df is None:
        return None

    columns = list(df.columns)
    lower_map = {str(column).lower(): column for column in columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]

    def normalize(value: str) -> str:
        return "".join(ch for ch in value.lower() if ch.isalnum())

    normalized_map = {normalize(str(column)): column for column in columns}
    for candidate in candidates:
        normalized = normalize(candidate)
        if normalized in normalized_map:
            return normalized_map[normalized]

    return None


def _to_number(value: Any) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).strip().replace(",", "")
    if text.endswith("%"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        return None


def _prepare_segment_data(segments: pd.DataFrame | None) -> pd.DataFrame:
    if segments is None or segments.empty:
        return pd.DataFrame()

    segment_col = _find_column(segments, ["segment_name", "segment", "customer_segment"])
    cn_col = _find_column(segments, ["segment_name_cn"])
    count_col = _find_column(segments, ["customer_count", "count"])
    share_col = _find_column(segments, ["customer_share", "percentage", "share", "share_pct"])
    aov_col = _find_column(segments, ["weighted_aov"])
    rfm_col = _find_column(segments, ["avg_rfm_score"])

    if not segment_col:
        return pd.DataFrame()

    prepared = pd.DataFrame()
    prepared["segment_name"] = segments[segment_col].astype(str)
    prepared["segment_label"] = (
        segments[cn_col].astype(str)
        if cn_col
        else prepared["segment_name"].map(SEGMENT_CN).fillna(prepared["segment_name"])
    )

    if count_col:
        prepared["customer_count"] = pd.to_numeric(segments[count_col], errors="coerce").fillna(0).astype(int)
    else:
        prepared["customer_count"] = 0

    if share_col:
        share_values = segments[share_col].map(_to_number)
        prepared["share_pct"] = pd.to_numeric(share_values, errors="coerce")
    else:
        total = prepared["customer_count"].sum()
        prepared["share_pct"] = (
            prepared["customer_count"] / total * 100 if total else 0
        )
    prepared["share_pct"] = prepared["share_pct"].fillna(0)
    if prepared["share_pct"].max() <= 1:
        prepared["share_pct"] = prepared["share_pct"] * 100

    prepared["weighted_aov"] = (
        pd.to_numeric(segments[aov_col], errors="coerce").fillna(0) if aov_col else 0
    )
    prepared["avg_rfm_score"] = (
        pd.to_numeric(segments[rfm_col], errors="coerce").fillna(0) if rfm_col else 0
    )

    return prepared.sort_values("customer_count", ascending=False).reset_index(drop=True)


def _run_project_command(args: list[str], timeout: int = 180) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [sys.executable, *args],
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


def _show_sidebar_result(result: dict[str, Any]) -> None:
    if result.get("status") == "success":
        st.sidebar.success("执行完成")
    elif result.get("status") == "timeout":
        st.sidebar.warning("执行超时")
    else:
        st.sidebar.error("执行失败")


def _render_sidebar() -> tuple[str, str]:
    st.sidebar.header("控制台")
    demo_case = st.sidebar.selectbox("Demo Case", ["baseline_original", "apparel_vip_shift"], index=0)
    provider = st.sidebar.selectbox("Provider", ["mock", "siliconflow"], index=0)

    if st.sidebar.button("应用数据源", use_container_width=True):
        result = _run_project_command(["scripts/apply_raw_case.py", demo_case], timeout=120)
        st.session_state["last_command_result"] = result
        _show_sidebar_result(result)

    if st.sidebar.button("运行分析流水线", use_container_width=True):
        result = _run_project_command(["run_pipeline.py", "--provider", provider], timeout=240)
        st.session_state["last_command_result"] = result
        _show_sidebar_result(result)

    if st.sidebar.button("运行评估测试", use_container_width=True):
        result = _run_project_command(["eval/run_eval.py"], timeout=120)
        st.session_state["last_command_result"] = result
        _show_sidebar_result(result)

    return demo_case, provider


def _metric_card(label: str, value: str, sub: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(value)}</div>
            <div class="metric-sub">{html.escape(sub)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _largest_segment(prepared_segments: pd.DataFrame) -> tuple[str, int]:
    if prepared_segments.empty:
        return "暂无数据", 0
    row = prepared_segments.sort_values("customer_count", ascending=False).iloc[0]
    return str(row["segment_label"]), int(row["customer_count"])


def _segment_count(prepared_segments: pd.DataFrame, segment_name: str) -> int:
    if prepared_segments.empty:
        return 0
    matched = prepared_segments[prepared_segments["segment_name"] == segment_name]
    if matched.empty:
        return 0
    return int(matched.iloc[0]["customer_count"])


def _render_kpi_cards(demo_case: str, prepared_segments: pd.DataFrame, fact: pd.DataFrame | None) -> None:
    total_users = int(prepared_segments["customer_count"].sum()) if not prepared_segments.empty else 0
    if total_users == 0 and fact is not None:
        total_users = len(fact)
    largest_name, largest_count = _largest_segment(prepared_segments)
    high_value_count = _segment_count(prepared_segments, "High-value Customers")
    churn_count = _segment_count(prepared_segments, "Churn-risk Customers")

    cols = st.columns(5)
    with cols[0]:
        _metric_card("当前数据场景", demo_case)
    with cols[1]:
        _metric_card("总用户数", f"{total_users:,}")
    with cols[2]:
        _metric_card("最大客户分群", largest_name, f"{largest_count:,} 人")
    with cols[3]:
        _metric_card("高价值用户数", f"{high_value_count:,}")
    with cols[4]:
        _metric_card("流失风险用户数", f"{churn_count:,}")


def _bar_chart(data: pd.DataFrame, x: str, y: str, title: str, color: str = BAR) -> None:
    if data.empty or x not in data.columns or y not in data.columns:
        st.info("当前数据不足，暂无法生成图表。")
        return

    if alt is not None:
        chart = (
            alt.Chart(data)
            .mark_bar(color=color, cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X(f"{x}:N", sort="-y", title=None, axis=alt.Axis(labelAngle=-25)),
                y=alt.Y(f"{y}:Q", title=None),
                tooltip=[
                    alt.Tooltip(f"{x}:N", title="分群"),
                    alt.Tooltip(f"{y}:Q", title=title, format=",.2f"),
                ],
            )
            .properties(height=280)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.bar_chart(data.set_index(x)[y])


def _share_chart(data: pd.DataFrame) -> None:
    if data.empty or "share_pct" not in data.columns:
        st.info("当前数据不足，暂无法生成占比图。")
        return

    if alt is None:
        _bar_chart(data, "segment_label", "share_pct", "分群占比", BAR_2)
        return

    chart = (
        alt.Chart(data)
        .mark_arc(innerRadius=55, outerRadius=98)
        .encode(
            theta=alt.Theta("share_pct:Q", title="分群占比"),
            color=alt.Color(
                "segment_label:N",
                scale=alt.Scale(range=PALETTE),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("segment_label:N", title="分群"),
                alt.Tooltip("share_pct:Q", title="占比", format=".1f"),
                alt.Tooltip("customer_count:Q", title="人数", format=","),
            ],
        )
        .properties(height=280)
    )
    st.altair_chart(chart, use_container_width=True)


def _render_segment_visuals(prepared_segments: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">客户分群结构</div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 0.85])
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("分群人数")
        _bar_chart(prepared_segments, "segment_label", "customer_count", "客户数", BAR)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("分群占比")
        _share_chart(prepared_segments)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Weighted AOV by Segment")
    _bar_chart(prepared_segments, "segment_label", "weighted_aov", "Weighted AOV", BAR_2)
    st.markdown("</div>", unsafe_allow_html=True)


def _eval_summary_values() -> tuple[str, int, str]:
    eval_results = _load_csv(EVAL_RESULTS_PATH)
    if eval_results is None or eval_results.empty:
        return "未生成", 0, "暂无结果"

    pass_columns = [column for column in eval_results.columns if column.endswith("_pass")]
    if not pass_columns:
        return "未生成", len(eval_results), "暂无结果"

    row_pass = eval_results[pass_columns].all(axis=1)
    pass_rate = f"{row_pass.mean() * 100:.1f}%"
    last_result = "通过" if bool(row_pass.iloc[-1]) else "未通过"
    return pass_rate, len(eval_results), last_result


def _render_eval_snapshot() -> None:
    pass_rate, total_cases, last_result = _eval_summary_values()
    cols = st.columns(3)
    with cols[0]:
        _metric_card("Eval Pass Rate", pass_rate)
    with cols[1]:
        _metric_card("Total Cases", str(total_cases))
    with cols[2]:
        _metric_card("Last Eval Result", last_result)


def _render_insight_card(row: dict[str, Any]) -> None:
    title = str(row.get("insight_title", "未命名洞察"))
    segment = str(row.get("segment_name", "N/A"))
    status = str(row.get("review_status", "N/A"))
    text = str(row.get("insight_text", ""))

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{html.escape(title)}</div>
            <div class="insight-meta">关联分群：{html.escape(segment)}　|　复核状态：{html.escape(status)}</div>
            <div class="insight-body">{html.escape(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_insight_cards(insights: pd.DataFrame | None, limit: int | None = None) -> None:
    if insights is None or insights.empty:
        st.warning("未找到经营洞察输出。请先运行分析流水线。")
        return

    rows = insights.to_dict(orient="records")
    if limit is not None:
        rows = rows[:limit]
    for row in rows:
        _render_insight_card(row)


def _business_rfm_answer(prepared_segments: pd.DataFrame) -> str:
    if prepared_segments.empty:
        return "当前没有可用的 RFM 分群结果。请先运行分析流水线。"

    total = int(prepared_segments["customer_count"].sum())
    largest = prepared_segments.sort_values("customer_count", ascending=False).iloc[0]
    high_value = _segment_count(prepared_segments, "High-value Customers")
    churn = _segment_count(prepared_segments, "Churn-risk Customers")
    potential = _segment_count(prepared_segments, "Potential Customers")

    return f"""
### 结论
当前数据已形成清晰的 RFM 客户分层：最大分群是 **{largest['segment_label']}**，共有 **{int(largest['customer_count'])}** 人；高价值用户共有 **{high_value}** 人，流失风险用户共有 **{churn}** 人。

### 关键数据
- 总用户数：**{total}**
- 高价值用户：**{high_value}**
- 潜力用户：**{potential}**
- 流失风险用户：**{churn}**

### 业务建议
- 优先保护高价值用户，围绕会员权益和高价值品类做留存。
- 对潜力用户重点设计复购激励，推动从低频购买向稳定复购转化。
- 对流失风险用户采用召回和服务跟进，避免把历史高价值客户简单视为低价值沉默用户。
"""


def _render_answer_data(prepared_segments: pd.DataFrame, result: AgentResult) -> None:
    if result.intent != "rfm_summary_question":
        return

    st.markdown('<div class="section-title">关键指标</div>', unsafe_allow_html=True)
    display_cols = ["segment_label", "customer_count", "share_pct", "weighted_aov", "avg_rfm_score"]
    table = prepared_segments[display_cols].rename(
        columns={
            "segment_label": "客户分群",
            "customer_count": "人数",
            "share_pct": "占比",
            "weighted_aov": "Weighted AOV",
            "avg_rfm_score": "Avg RFM Score",
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)
    _bar_chart(prepared_segments, "segment_label", "customer_count", "客户数", BAR)


def _render_business_question(provider: str, prepared_segments: pd.DataFrame) -> None:
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

    if st.button("生成经营分析", type="primary"):
        if not effective_question:
            st.warning("请输入或选择一个业务问题。")
            return

        result = run_agent_request(
            AgentRequest(
                question=effective_question,
                dry_run=True,
                provider=provider,
                trace_enabled=False,
            )
        )
        st.session_state["last_agent_result"] = result

        if result.intent == "rfm_summary_question":
            answer = _business_rfm_answer(prepared_segments)
        else:
            answer = result.final_answer

        st.markdown('<div class="answer-card">', unsafe_allow_html=True)
        st.markdown(answer)
        st.markdown("</div>", unsafe_allow_html=True)

        _render_answer_data(prepared_segments, result)
        st.markdown(
            '<div class="muted">数据来源：data/processed/customer_segments.csv</div>',
            unsafe_allow_html=True,
        )


def _render_overview_tab(prepared_segments: pd.DataFrame, insights: pd.DataFrame | None) -> None:
    _render_segment_visuals(prepared_segments)
    st.markdown('<div class="section-title">AI 经营洞察</div>', unsafe_allow_html=True)
    _render_insight_cards(insights, limit=5)
    st.markdown('<div class="section-title">评估概览</div>', unsafe_allow_html=True)
    _render_eval_snapshot()


def _render_insights_tab(insights: pd.DataFrame | None) -> None:
    st.markdown('<div class="section-title">经营洞察输出</div>', unsafe_allow_html=True)
    _render_insight_cards(insights)
    st.markdown(
        '<div class="muted">Power BI 刷新后可读取 outputs/powerbi_llm_insights.csv 用于 AI Insight Box。</div>',
        unsafe_allow_html=True,
    )


def _eval_detail_table() -> pd.DataFrame | None:
    return _load_csv(EVAL_RESULTS_PATH)


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


def _metadata_summary(metadata: dict[str, Any] | None) -> dict[str, Any]:
    if metadata is None:
        return {}
    keys = [
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
    return {key: metadata.get(key) for key in keys}


def _render_developer_console(
    segments: pd.DataFrame | None,
    fact: pd.DataFrame | None,
    insights: pd.DataFrame | None,
    metadata: dict[str, Any] | None,
) -> None:
    with st.expander("技术细节（开发者模式）", expanded=False):
        result = st.session_state.get("last_agent_result")
        if result is not None:
            st.subheader("Agent Routing")
            st.write(
                {
                    "Intent": result.intent,
                    "Tools": result.selected_tools,
                    "Risk Level": result.risk_level,
                    "Dry Run": result.dry_run,
                    "Status": result.status,
                }
            )
        else:
            st.caption("尚未在本页面发起业务问答。")

        st.subheader("Run Metadata 摘要")
        st.json(_metadata_summary(metadata))

        st.subheader("Eval Harness 详细结果")
        eval_detail = _eval_detail_table()
        if eval_detail is None:
            st.caption("未找到 eval/eval_results.csv。")
        else:
            st.dataframe(eval_detail, use_container_width=True)

        st.subheader("最近 Trace")
        traces = _read_recent_traces()
        if traces:
            st.json(traces)
        else:
            st.caption("未找到 logs/agent_runs.jsonl。")

        st.subheader("原始 CSV 预览")
        preview_tabs = st.tabs(["customer_segments", "fact_user_behavior_scored", "powerbi_llm_insights"])
        with preview_tabs[0]:
            if segments is not None:
                st.dataframe(segments.head(20), use_container_width=True)
        with preview_tabs[1]:
            if fact is not None:
                st.dataframe(fact.head(20), use_container_width=True)
        with preview_tabs[2]:
            if insights is not None:
                st.dataframe(insights.head(20), use_container_width=True)

        command_result = st.session_state.get("last_command_result")
        if command_result is not None:
            st.subheader("最近执行结果")
            st.json(command_result)


def main() -> None:
    st.set_page_config(page_title="AI BI 智能分析工作台", layout="wide")
    _inject_css()

    demo_case, provider = _render_sidebar()
    segments = _load_csv(CUSTOMER_SEGMENTS_PATH)
    fact = _load_csv(FACT_SCORED_PATH)
    insights = _load_csv(POWERBI_INSIGHTS_PATH)
    metadata = _load_metadata()
    prepared_segments = _prepare_segment_data(segments)

    st.markdown(
        """
        <div class="hero">
            <h1>AI BI 智能分析工作台</h1>
            <p>从数据源切换到客户分群、经营洞察与自然语言问答的自动化分析闭环</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_kpi_cards(demo_case, prepared_segments, fact)

    overview_tab, ask_tab, insights_tab = st.tabs(["经营总览", "业务问答", "洞察输出"])
    with overview_tab:
        _render_overview_tab(prepared_segments, insights)
    with ask_tab:
        st.markdown('<div class="section-title">业务问答</div>', unsafe_allow_html=True)
        _render_business_question(provider, prepared_segments)
    with insights_tab:
        _render_insights_tab(insights)

    _render_developer_console(segments, fact, insights, metadata)


if __name__ == "__main__":
    main()
