from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from llm_client import LLMResponse, call_llm, insight_summary_cn, recommended_action_cn


ROOT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT_DIR / "outputs"
LEGACY_OUTPUT_DIR = ROOT_DIR / "llm_agent" / "outputs"

OUTPUT_MD = OUTPUT_DIR / "segment_insights.md"
OUTPUT_CSV = OUTPUT_DIR / "powerbi_llm_insights.csv"
LEGACY_OUTPUT_MD = LEGACY_OUTPUT_DIR / "segment_insights.md"
LEGACY_OUTPUT_CSV = LEGACY_OUTPUT_DIR / "powerbi_llm_insights.csv"

SEGMENT_CN = {
    "High-value Customers": "高价值用户",
    "Potential Customers": "潜力用户",
    "Churn-risk Customers": "流失风险用户",
    "Regular Retained Customers": "一般保持用户",
    "Other Customers": "其他用户",
}

ACTION_CN = {
    "Stabilize": "稳定留存",
    "Convert": "转化提升",
    "Recover": "召回修复",
    "Upsell": "追加销售",
    "Nurture": "低成本培育",
}

ROLE_CN = {
    "Core profit engine": "核心利润来源",
    "Growth engine": "增长转化池",
    "Dormant premium assets": "高价值沉睡资产",
    "Traffic foundation": "稳定流量基本盘",
    "Long-tail users": "长尾培育人群",
}

KEY_ISSUE_CN = {
    "Need loyalty protection and VIP retention": "需要重点做忠诚度保护和 VIP 留存",
    "Large base but low repurchase frequency": "用户基数较大，但复购频次偏低",
    "High historical spending but low recent engagement": "历史消费较高，但近期互动不足",
    "Frequent buyers with relatively lower spending": "购买较频繁，但单体消费价值相对较低",
    "Low engagement and limited short-term value": "互动较低，短期价值有限",
}

CROSS_INSIGHT_CN = {
    "Elite Customer Segment": "高客单细分人群",
    "Regional Category Opportunity": "区域品类机会",
    "Pareto Value Concentration": "价值集中度",
    "Churn Recovery": "流失召回机会",
    "High-value Category Focus": "高价值品类聚焦",
}


@dataclass
class InsightGenerationResult:
    llm_response: LLMResponse
    output_files: dict[str, Path]


def build_prompt(structured_summary: dict[str, Any]) -> str:
    summary_json = json.dumps(structured_summary, ensure_ascii=False, indent=2)

    return f"""你正在为电商客户分群 Dashboard 生成中文 BI 决策支持内容。

只能使用下方 structured summary。不要编造数字、百分比、分群规模、客户数、产品品类、排名、年龄、AOV、RFM score、Value Proxy Score、最近活跃、购买频次、消费金额、活动周期、折扣率或 model/provider 信息。

需要业务数字时，请直接复制 structured summary 中已有的数字，优先使用 summary 中已展示的精确值。不要估算、重算、外推或创造新的 KPI。如果缺少某个有用数字，请说明需要人工复核，不要自行补充。

请使用中文输出。尽量使用无编号 bullet points。标题可以编号，但标题编号不是业务指标。

返回一份简洁 Markdown 草稿，包含以下部分：
- 核心客户分群结果
- 高价值客户洞察
- 流失风险客户洞察
- 营销建议
- Human Review 人工复核提醒

Structured summary:
```json
{summary_json}
```
"""


def markdown_table(records: list[dict[str, Any]], columns: list[str]) -> str:
    if not records:
        return "No segment records were generated."

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for record in records:
        rows.append("| " + " | ".join(str(record.get(column, "")) for column in columns) + " |")
    return "\n".join([header, separator, *rows])


def find_segment(summary: dict[str, Any], segment_name: str) -> dict[str, Any]:
    for segment in summary.get("segment_results", []):
        if segment.get("segment") == segment_name:
            return dict(segment)
    return {}


def find_insight(summary: dict[str, Any], keyword: str) -> dict[str, Any]:
    for insight in summary.get("cross_dimensional_insights", []):
        if keyword.lower() in str(insight.get("insight_name", "")).lower():
            return dict(insight)
    return {}


def segment_cn(segment_name: str) -> str:
    return SEGMENT_CN.get(segment_name, segment_name)


def action_cn(action_priority: str) -> str:
    return ACTION_CN.get(action_priority, action_priority)


def role_cn(role: str) -> str:
    return ROLE_CN.get(role, role)


def key_issue_cn(issue: str) -> str:
    return KEY_ISSUE_CN.get(issue, issue)


def cross_insight_title_cn(insight_name: str) -> str:
    return CROSS_INSIGHT_CN.get(insight_name, insight_name)


def segment_sentence(segment: dict[str, Any]) -> str:
    if not segment:
        return "未生成对应分群数据，需要人工复核。"

    segment_name = str(segment.get("segment", ""))
    return (
        f"{segment_name}（{segment_cn(segment_name)}）包含 {segment.get('customer_count')} 个用户，"
        f"占比 {segment.get('share')}。Weighted AOV 为 {segment.get('weighted_aov')}，"
        f"Avg RFM Score 为 {segment.get('avg_rfm_score')}，Avg Value Proxy Score 为 "
        f"{segment.get('avg_value_proxy_score')}。核心问题：{key_issue_cn(str(segment.get('key_issue', '')))}。"
    )


def build_markdown_report(structured_summary: dict[str, Any], llm_response: LLMResponse) -> str:
    data_sources = structured_summary.get("data_sources", [])
    source_lines = "\n".join(
        f"- {source.get('path')}（raw rows: {source.get('row_count')}，cleaned rows: {source.get('cleaned_row_count')}，encoding: {source.get('encoding')}）"
        for source in data_sources
    )

    segment_records = structured_summary.get("segment_results", [])
    core_table = markdown_table(
        segment_records,
        [
            "segment",
            "customer_count",
            "share",
            "weighted_aov",
            "avg_rfm_score",
            "avg_value_proxy_score",
            "category_preference",
            "action_priority",
        ],
    )

    high_value = find_segment(structured_summary, "High-value Customers")
    churn = find_segment(structured_summary, "Churn-risk Customers")
    elite = find_insight(structured_summary, "Elite")
    regional = find_insight(structured_summary, "Regional")
    pareto = find_insight(structured_summary, "Pareto")

    provider_note = (
        f"requested_provider: {llm_response.requested_provider}; provider: "
        f"{llm_response.provider}; model: {llm_response.model}; api_reached: "
        f"{llm_response.api_reached}; validation_passed: {llm_response.validation_passed}; "
        f"fallback_used: {llm_response.fallback_used}; retry_count: "
        f"{llm_response.retry_count}; error_type: {llm_response.error_type}."
    )
    if llm_response.error:
        provider_note += f" error: {llm_response.error}"

    summary_json = json.dumps(structured_summary, ensure_ascii=False, indent=2)

    return f"""# AI 辅助 BI 决策工作流 - 客户分群洞察

## 项目运行时间
- UTC: {structured_summary.get('run_time_utc')}
- {provider_note}

## 数据来源
{source_lines}
- raw_row_count: {structured_summary.get('raw_row_count')}
- cleaned_row_count: {structured_summary.get('cleaned_row_count')}
- processed_customer_count: {structured_summary.get('processed_customer_count')}

## 核心客户分群结果
{core_table}

## 高价值客户洞察
{segment_sentence(high_value)}

{insight_summary_cn(elite)}

## 流失风险客户洞察
{segment_sentence(churn)}

建议来源：{recommended_action_cn(find_insight(structured_summary, 'Churn'))}

## 营销建议
{llm_response.text.strip()}

补充的结构化数据信号：
- {insight_summary_cn(regional)}
- {insight_summary_cn(pareto)}

## Human Review 人工复核提醒
- 执行前请复核分群定义、raw 数据新鲜度和活动资格。
- 请结合毛利、库存、物流、客服和合规约束复核 AI 生成建议。
- 本报告只支持 BI 决策准备，不代表自动批准面向客户的运营动作。

## LLM 使用的 Structured Summary
```json
{summary_json}
```
"""


def priority_for_action(action_priority: str) -> str:
    mapping = {
        "Recover": "高",
        "Stabilize": "高",
        "Convert": "中",
        "Upsell": "中",
        "Nurture": "低",
    }
    return mapping.get(action_priority, "中")


def build_powerbi_insight_csv(structured_summary: dict[str, Any]) -> pd.DataFrame:
    generated_at = structured_summary.get("run_time_utc")
    rows: list[dict[str, Any]] = []

    for segment in structured_summary.get("segment_results", []):
        action_priority = str(segment.get("action_priority", ""))
        segment_name = str(segment.get("segment", ""))
        rows.append(
            {
                "insight_title": f"{segment_cn(segment_name)} - {action_cn(action_priority)}",
                "insight_text": (
                    f"{segment_name}（{segment_cn(segment_name)}）包含 {segment.get('customer_count')} 个用户，"
                    f"占比 {segment.get('share')}。Weighted AOV 为 {segment.get('weighted_aov')}；"
                    f"Avg RFM Score 为 {segment.get('avg_rfm_score')}；Value Proxy Score 为 "
                    f"{segment.get('avg_value_proxy_score')}。核心问题："
                    f"{key_issue_cn(str(segment.get('key_issue', '')))}。建议方向："
                    f"{action_cn(action_priority)}。"
                ),
                "segment_name": segment_name,
                "priority": priority_for_action(action_priority),
                "review_status": "待人工复核",
                "generated_at": generated_at,
            }
        )

    for insight in structured_summary.get("cross_dimensional_insights", []):
        rows.append(
            {
                "insight_title": cross_insight_title_cn(str(insight.get("insight_name", ""))),
                "insight_text": (
                    f"{insight_summary_cn(insight)} 建议动作：{recommended_action_cn(insight)}"
                ),
                "segment_name": "Cross-dimensional",
                "priority": "中",
                "review_status": "待人工复核",
                "generated_at": generated_at,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "insight_title",
            "insight_text",
            "segment_name",
            "priority",
            "review_status",
            "generated_at",
        ],
    )


def write_text_to_both_locations(text: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(text, encoding="utf-8")
    LEGACY_OUTPUT_MD.write_text(text, encoding="utf-8")


def write_csv_to_both_locations(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    df.to_csv(LEGACY_OUTPUT_CSV, index=False, encoding="utf-8-sig")


def generate_outputs(
    structured_summary: dict[str, Any],
    provider: str | None = None,
) -> InsightGenerationResult:
    prompt = build_prompt(structured_summary)
    llm_response = call_llm(prompt, structured_summary, provider=provider)

    markdown_report = build_markdown_report(structured_summary, llm_response)
    powerbi_df = build_powerbi_insight_csv(structured_summary)

    write_text_to_both_locations(markdown_report)
    write_csv_to_both_locations(powerbi_df)

    return InsightGenerationResult(
        llm_response=llm_response,
        output_files={
            "segment_insights": OUTPUT_MD,
            "powerbi_llm_insights": OUTPUT_CSV,
            "legacy_segment_insights": LEGACY_OUTPUT_MD,
            "legacy_powerbi_llm_insights": LEGACY_OUTPUT_CSV,
        },
    )


def main() -> None:
    from prepare_processed_data import build_structured_summary, run_processing, utc_now_iso

    run_time_utc = utc_now_iso()
    processed = run_processing()
    structured_summary = build_structured_summary(processed, run_time_utc=run_time_utc)
    result = generate_outputs(structured_summary)

    print(f"Provider: {result.llm_response.provider}")
    print(f"Model: {result.llm_response.model}")
    print(f"API reached: {result.llm_response.api_reached}")
    print(f"Validation passed: {result.llm_response.validation_passed}")
    print(f"Fallback used: {result.llm_response.fallback_used}")
    print(f"Retry count: {result.llm_response.retry_count}")
    print(f"Error type: {result.llm_response.error_type}")
    print(f"Saved: {OUTPUT_MD}")
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
