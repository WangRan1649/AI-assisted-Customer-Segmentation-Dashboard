from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from llm_client import LLMResponse, call_llm


ROOT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT_DIR / "outputs"
LEGACY_OUTPUT_DIR = ROOT_DIR / "llm_agent" / "outputs"

OUTPUT_MD = OUTPUT_DIR / "segment_insights.md"
OUTPUT_CSV = OUTPUT_DIR / "powerbi_llm_insights.csv"
LEGACY_OUTPUT_MD = LEGACY_OUTPUT_DIR / "segment_insights.md"
LEGACY_OUTPUT_CSV = LEGACY_OUTPUT_DIR / "powerbi_llm_insights.csv"


@dataclass
class InsightGenerationResult:
    llm_response: LLMResponse
    output_files: dict[str, Path]


def build_prompt(structured_summary: dict[str, Any]) -> str:
    summary_json = json.dumps(structured_summary, ensure_ascii=False, indent=2)

    return f"""You are generating BI decision support content for an e-commerce customer segmentation dashboard.

Use only the structured summary below. Do not invent numbers, percentages, segment sizes, customer counts, product categories, rankings, ages, AOV values, RFM scores, Value Proxy Scores, recency values, frequency values, spending amounts, campaign timing, discount rates, or model/provider details.

When you need a business number, copy it from the structured summary. Prefer exact values already shown in the summary. Do not estimate, recalculate, extrapolate, or create new KPI values. If a useful business number is absent, say that human review is required instead of filling the gap.

Use bullet points without numeric prefixes where practical. Section titles may be numbered, but numbered titles are not business metrics.

Return a concise Markdown draft with these sections:
- Core Customer Segment Results
- High-value Customer Insight
- Churn-risk Customer Insight
- Marketing Recommendations
- Human Review Reminder

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


def segment_sentence(segment: dict[str, Any]) -> str:
    if not segment:
        return "No matching segment was generated; this requires human review."
    return (
        f"{segment.get('segment')} contains {segment.get('customer_count')} customers "
        f"({segment.get('share')}). Weighted AOV is {segment.get('weighted_aov')}, "
        f"average RFM score is {segment.get('avg_rfm_score')}, and average Value Proxy Score is "
        f"{segment.get('avg_value_proxy_score')}. Key issue: {segment.get('key_issue')}."
    )


def build_markdown_report(structured_summary: dict[str, Any], llm_response: LLMResponse) -> str:
    data_sources = structured_summary.get("data_sources", [])
    source_lines = "\n".join(
        f"- {source.get('path')} (raw rows: {source.get('row_count')}, cleaned rows: {source.get('cleaned_row_count')}, encoding: {source.get('encoding')})"
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
        f"Requested provider: {llm_response.requested_provider}; actual provider: "
        f"{llm_response.provider}; model: {llm_response.model}; api reached: "
        f"{llm_response.api_reached}; validation passed: {llm_response.validation_passed}; "
        f"fallback used: {llm_response.fallback_used}."
    )
    if llm_response.error:
        provider_note += f" Error: {llm_response.error}"

    summary_json = json.dumps(structured_summary, ensure_ascii=False, indent=2)

    return f"""# AI-assisted BI Decision Workflow - Segment Insights

## Project Run Time
- UTC: {structured_summary.get('run_time_utc')}
- {provider_note}

## Data Source
{source_lines}
- Raw row count: {structured_summary.get('raw_row_count')}
- Cleaned row count: {structured_summary.get('cleaned_row_count')}
- Processed customer count: {structured_summary.get('processed_customer_count')}

## Core Customer Segment Results
{core_table}

## High-value Customer Insights
{segment_sentence(high_value)}

{elite.get('key_finding', '')}

## Churn-risk Customer Insights
{segment_sentence(churn)}

Recommended action source: {find_insight(structured_summary, 'Churn').get('recommended_action', 'No churn recovery recommendation generated.')}

## Marketing Recommendations
{llm_response.text.strip()}

Additional data-backed signals:
- {regional.get('key_finding', 'No regional opportunity insight was generated.')}
- {pareto.get('key_finding', 'No value concentration insight was generated.')}

## Human Review Reminder
- Review segment definitions, raw data freshness, and campaign eligibility before execution.
- Validate all AI-generated recommendations against margin, inventory, logistics, and compliance constraints.
- This report supports BI decision preparation only; it does not approve customer-facing actions.

## Structured Summary Used By LLM
```json
{summary_json}
```
"""


def priority_for_action(action_priority: str) -> str:
    mapping = {
        "Recover": "High",
        "Stabilize": "High",
        "Convert": "Medium",
        "Upsell": "Medium",
        "Nurture": "Low",
    }
    return mapping.get(action_priority, "Medium")


def build_powerbi_insight_csv(structured_summary: dict[str, Any]) -> pd.DataFrame:
    generated_at = structured_summary.get("run_time_utc")
    rows: list[dict[str, Any]] = []

    for segment in structured_summary.get("segment_results", []):
        action_priority = str(segment.get("action_priority", ""))
        rows.append(
            {
                "insight_title": f"{segment.get('segment')} - {action_priority}",
                "insight_text": (
                    f"{segment.get('segment')} includes {segment.get('customer_count')} customers "
                    f"({segment.get('share')}). Weighted AOV is {segment.get('weighted_aov')}; "
                    f"average RFM score is {segment.get('avg_rfm_score')}; Value Proxy Score is "
                    f"{segment.get('avg_value_proxy_score')}. Key issue: {segment.get('key_issue')}."
                ),
                "segment_name": segment.get("segment"),
                "priority": priority_for_action(action_priority),
                "review_status": "Pending human review",
                "generated_at": generated_at,
            }
        )

    for insight in structured_summary.get("cross_dimensional_insights", []):
        rows.append(
            {
                "insight_title": insight.get("insight_name"),
                "insight_text": (
                    f"{insight.get('key_finding')} Business meaning: "
                    f"{insight.get('business_meaning')} Recommended action: "
                    f"{insight.get('recommended_action')}"
                ),
                "segment_name": "Cross-dimensional",
                "priority": "Medium",
                "review_status": "Pending human review",
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
    print(f"Saved: {OUTPUT_MD}")
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
