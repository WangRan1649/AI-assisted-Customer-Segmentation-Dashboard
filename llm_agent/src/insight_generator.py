import json
from pathlib import Path

import pandas as pd

from llm_client import call_llm


ROOT_DIR = Path(__file__).resolve().parents[2]

SEGMENT_FILE = ROOT_DIR / "data" / "processed" / "customer_segments.csv"
INSIGHT_FILE = ROOT_DIR / "data" / "processed" / "cross_dimensional_insights.csv"

OUTPUT_MD = ROOT_DIR / "llm_agent" / "outputs" / "segment_insights.md"
OUTPUT_CSV = ROOT_DIR / "llm_agent" / "outputs" / "powerbi_llm_insights.csv"


def load_project_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load structured customer segment data and cross-dimensional insights."""

    segments = pd.read_csv(SEGMENT_FILE)
    insights = pd.read_csv(INSIGHT_FILE)

    return segments, insights


def find_record(df: pd.DataFrame, column: str, keyword: str) -> dict:
    """
    Find the first row whose column contains the keyword.
    Return an empty dict if not found.
    """

    matched = df[df[column].astype(str).str.contains(keyword, case=False, na=False)]

    if matched.empty:
        return {}

    return matched.iloc[0].to_dict()


def build_prompt(segments: pd.DataFrame, insights: pd.DataFrame) -> str:
    """Build a business prompt for the LLM based on structured CSV data."""

    segment_records = segments.to_dict(orient="records")
    insight_records = insights.to_dict(orient="records")

    prompt = f"""
You are analyzing an e-commerce customer segmentation dashboard.

Project context:
- The dashboard is based on RFM-style customer segmentation.
- The business goal is to improve customer retention, potential customer conversion, and marketing decision-making.
- The AI layer should not replace business users. It should generate recommendations for human review.

Customer segment data:
{json.dumps(segment_records, ensure_ascii=False, indent=2)}

Cross-dimensional business insights:
{json.dumps(insight_records, ensure_ascii=False, indent=2)}

Please generate a business-ready AI insight report in English with the following structure:

# AI-generated Customer Segmentation Insights

## 1. Executive Summary
Summarize the most important business findings in 4-6 bullet points.

## 2. Segment Interpretation
For each customer segment, explain:
- Business meaning
- Key risk or opportunity
- Recommended marketing action

## 3. Priority Actions
Provide 5 concrete actions the marketing or operations team should take.

## 4. Human-in-the-loop Review Checklist
List what business users must verify before executing AI-generated recommendations.

Important rules:
- Use the real numbers provided, such as 27.7%, 27.0%, 22.0%, 15.0%, and AOV above ¥3000.
- Mention the 45-year-old male elite customer insight.
- Mention the rural Books category and knowledge penetration opportunity.
- Do not invent unsupported numbers.
- Keep the tone professional and suitable for an international business interview portfolio.
"""

    return prompt


def build_powerbi_insight_csv(segments: pd.DataFrame, insights: pd.DataFrame) -> pd.DataFrame:
    """
    Build a Power BI-ready insight table automatically.

    This avoids manually converting the Markdown report into CSV.
    The CSV is designed for the LLM Insight Box in Power BI.
    """

    high_value = find_record(segments, "segment", "High-value")
    potential = find_record(segments, "segment", "Potential")
    churn = find_record(segments, "segment", "Churn-risk")
    regular = find_record(segments, "segment", "Regular")

    middle_age = find_record(insights, "insight_name", "Middle-aged")
    knowledge = find_record(insights, "insight_name", "Knowledge")
    pareto = find_record(insights, "insight_name", "Pareto")
    churn_recovery = find_record(insights, "insight_name", "Churn")

    rows = [
        {
            "insight_title": "Churn-risk Recovery",
            "insight_text": (
                f"{churn.get('share', '22.0%')} of customers are at churn risk. "
                f"This segment is described as {churn.get('business_role', 'dormant premium assets')} "
                f"with {churn.get('monetary_range', 'historically high AOV above ¥3000')}. "
                f"Recommended action: {churn_recovery.get('recommended_action', 'build win-back campaigns with logistics follow-up and electronics upgrade reminders')}."
            ),
            "review_status": "Pending human review",
        },
        {
            "insight_title": "Middle-aged Elite Strategy",
            "insight_text": (
                f"{middle_age.get('key_finding', 'Male customers around age 45 peak in both customer volume and AOV')}. "
                f"Business meaning: {middle_age.get('business_meaning', 'This group is the core profit driver of the platform')}. "
                f"Recommended action: {middle_age.get('recommended_action', 'launch premium electronics campaigns with expert reviews and VIP services')}."
            ),
            "review_status": "Pending human review",
        },
        {
            "insight_title": "Rural Knowledge Penetration",
            "insight_text": (
                f"{knowledge.get('key_finding', 'Rural high-value customers show strong preference and high AOV in the Books category')}. "
                f"Business meaning: {knowledge.get('business_meaning', 'Rural market contains underexplored knowledge consumption demand')}. "
                f"Recommended action: {knowledge.get('recommended_action', 'create curated book bundles and knowledge-oriented content campaigns')}."
            ),
            "review_status": "Pending human review",
        },
        {
            "insight_title": "Potential Customer Conversion",
            "insight_text": (
                f"{potential.get('share', '27.0%')} of customers are potential customers. "
                f"They are the {potential.get('business_role', 'growth engine')} but currently show "
                f"{potential.get('key_issue', 'large base but low repurchase frequency')}. "
                f"Recommended action: use repurchase incentives, category bundles, and personalized recommendations to increase repeat purchases."
            ),
            "review_status": "Pending human review",
        },
        {
            "insight_title": "High-value Customer Protection",
            "insight_text": (
                f"{high_value.get('share', '27.7%')} of customers are high-value customers. "
                f"They are the {high_value.get('business_role', 'core profit engine')} with preference for "
                f"{high_value.get('category_preference', 'Apparel and Home')}. "
                f"Recommended action: build VIP retention, loyalty benefits, and premium product recommendations."
            ),
            "review_status": "Pending human review",
        },
        {
            "insight_title": "Pareto Value Focus",
            "insight_text": (
                f"{pareto.get('key_finding', 'Top 10% customers contribute more than 40% of GMV')}. "
                f"Business meaning: {pareto.get('business_meaning', 'Revenue is highly concentrated among premium customers')}. "
                f"Recommended action: {pareto.get('recommended_action', 'prioritize retention resources for top-tier customers')}."
            ),
            "review_status": "Pending human review",
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    segments, insights = load_project_data()
    prompt = build_prompt(segments, insights)

    print("Generating Markdown insight report through LLM or Mock LLM...")
    markdown_result = call_llm(prompt)

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(markdown_result, encoding="utf-8")

    print("Generating Power BI-ready insight CSV automatically...")
    powerbi_df = build_powerbi_insight_csv(segments, insights)
    powerbi_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"Done. Markdown report saved to: {OUTPUT_MD}")
    print(f"Done. Power BI insight CSV saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

