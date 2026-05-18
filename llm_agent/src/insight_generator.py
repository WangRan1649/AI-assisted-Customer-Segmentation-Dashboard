import json
from pathlib import Path

import pandas as pd

from llm_client import call_llm


ROOT_DIR = Path(__file__).resolve().parents[2]

SEGMENT_FILE = ROOT_DIR / "data" / "processed" / "customer_segments.csv"
INSIGHT_FILE = ROOT_DIR / "data" / "processed" / "cross_dimensional_insights.csv"
OUTPUT_FILE = ROOT_DIR / "llm_agent" / "outputs" / "segment_insights.md"


def load_project_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load structured customer segment data and cross-dimensional insights."""

    segments = pd.read_csv(SEGMENT_FILE)
    insights = pd.read_csv(INSIGHT_FILE)

    return segments, insights


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


def main() -> None:
    segments, insights = load_project_data()
    prompt = build_prompt(segments, insights)

    print("Calling LLM API...")
    result = call_llm(prompt)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(result, encoding="utf-8")

    print(f"Done. AI insight report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()