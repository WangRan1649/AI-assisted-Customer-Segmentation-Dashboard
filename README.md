# AI-assisted Customer Segmentation Dashboard V3

## Project Overview

This project is an **AI-assisted BI Decision Workflow for e-commerce customer segmentation**. It combines Python data processing, RFM-style customer analytics, SiliconFlow API-based LLM insight generation, and Power BI reporting.

V3 turns the project from a static customer segmentation dashboard into a repeatable decision workflow: when raw e-commerce data is replaced under `data/raw/`, one pipeline command regenerates processed customer segments, AI-assisted business insights, Power BI-readable insight tables, and auditable run metadata.

The system supports both **Mock mode** and **SiliconFlow API mode**. The V3 pipeline has been verified with SiliconFlow API using:

```text
requested_provider = siliconflow
provider = siliconflow
model = deepseek-ai/DeepSeek-V4-Flash
api_reached = True
validation_passed = True
fallback_used = False
error = None
raw_row_count = 1001
processed_customer_count = 1000
```

## V3 Upgrade Highlights

- Reads raw e-commerce CSV files from `data/raw/`.
- Cleans raw data and regenerates `data/processed/customer_segments.csv`.
- Generates `data/processed/fact_user_behavior_scored.csv` as the user-level scored fact table for Power BI main visuals.
- Calculates RFM metrics, weighted AOV, Value Proxy Score, customer segments, and cross-dimensional insights in Python.
- Builds a structured summary from Python-computed results before calling the LLM.
- Supports SiliconFlow API mode for real LLM-generated business wording.
- Keeps Mock mode for local demos, offline testing, and fallback output.
- Uses numeric validation to reduce unsupported business-number hallucination.
- Falls back to Mock output when API calls fail or validation fails.
- Writes `outputs/run_metadata.json` to audit provider, model, fallback status, validation status, raw rows, customer count, and generated files.

## Business Context

E-commerce teams often already have BI dashboards, but dashboards usually stop at visualization. Business users still need to interpret charts, identify customer risks, write summary reports, and design campaign actions.

This project addresses that gap by connecting BI metrics with an AI-assisted decision layer. Python remains responsible for the quantitative calculations, while the LLM converts structured data into marketing insights and human-reviewable recommendations.

The goal is not to replace analysts. The goal is to reduce repetitive reporting work and help business teams move from dashboard viewing to decision preparation.

## Current Customer Segment Results

The latest V3 run processed **1,001 raw rows** and generated **1,000 processed customers**.

| Segment | Customers | Share | Weighted AOV | Avg RFM Score | Action Priority |
|---|---:|---:|---:|---:|---|
| High-value Customers | 122 | 12.2% | 523.72 | 13.02 | Stabilize |
| Potential Customers | 292 | 29.2% | 1319.66 | 8.47 | Convert |
| Churn-risk Customers | 188 | 18.8% | 812.10 | 8.80 | Recover |
| Regular Retained Customers | 307 | 30.7% | 253.79 | 9.16 | Upsell |
| Other Customers | 91 | 9.1% | 289.51 | 6.02 | Nurture |

Current cross-dimensional insights:

- Female customers around age 51 show the highest weighted AOV: 1001.62.
- Suburban customers in the Apparel category show weighted AOV: 681.24.
- Top 10% users contribute approximately 18.6% of total spending.
- Churn-risk customers have strongest preference in Home & Kitchen.
- High-value customers show strongest preference in Apparel.

## Tech Stack

| Layer | Tools / Methods |
|---|---|
| Data Layer | CSV, Python, pandas |
| Metrics Layer | RFM, weighted AOV, Value Proxy Score |
| AI Layer | Mock provider, SiliconFlow API, structured prompt |
| Validation Layer | Numeric validation against Python structured summary |
| Output Layer | Markdown report, Power BI insight CSV, run metadata JSON |
| BI Layer | Power BI, DAX, refreshable CSV outputs |
| Governance | Fallback mechanism, human-in-the-loop review |

## Repository Structure

```text
AI-assisted-Customer-Segmentation-Dashboard/
|-- data/
|   |-- raw/
|   |-- processed/
|   `-- dictionary/
|-- docs/
|-- llm_agent/
|   |-- src/
|   |-- prompt_templates/
|   `-- outputs/
|-- outputs/
|-- portfolio/
|-- powerbi/
|-- sql/
|-- run_pipeline.py
|-- run_pipeline.ps1
|-- requirements.txt
|-- .env.example
|-- README.md
`-- README_CN.md
```

## One-click Pipeline

The V3 pipeline regenerates the main business artifacts in one run:

```text
data/raw/*.csv
        ->
Python cleaning and RFM/value scoring
        ->
data/processed/fact_user_behavior_scored.csv
data/processed/customer_segments.csv
        ->
Consistent segment counts for BI visuals and AI insights
        ->
Structured summary
        ->
Mock provider or SiliconFlow API
        ->
outputs/segment_insights.md
outputs/powerbi_llm_insights.csv
outputs/run_metadata.json
```

Generated files:

- `data/processed/fact_user_behavior_scored.csv`
- `data/processed/customer_segments.csv`
- `outputs/segment_insights.md`
- `outputs/powerbi_llm_insights.csv`
- `outputs/run_metadata.json`

For compatibility with the earlier Power BI prototype, AI insight outputs are also mirrored under `llm_agent/outputs/`.

## Mock Mode and SiliconFlow API Mode

The system supports two provider modes.

**Mock mode** is used for local demos, deterministic testing, and fallback output. It does not call any external API.

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider mock
```

**SiliconFlow API mode** calls the configured SiliconFlow-compatible chat completion endpoint and validates the returned business numbers before accepting the result.

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

## How to Configure `.env`

Create a local `.env` file in the project root. Do not commit `.env` because it contains secrets.

```env
LLM_PROVIDER=siliconflow
SILICONFLOW_API_KEY=your_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V4-Flash
```

For Mock mode:

```env
LLM_PROVIDER=mock
```

The provider can also be overridden per run with `--provider mock` or `--provider siliconflow`.

## How to Run Locally

From Windows PowerShell or Windows cmd:

```powershell
cd D:\chatgpt\AI-assisted-Customer-Segmentation-Dashboard
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run Mock mode:

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider mock
```

Run SiliconFlow API mode:

```powershell
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

You can also use the PowerShell helper:

```powershell
powershell -ExecutionPolicy Bypass -File run_pipeline.ps1
```

## How to Verify Real API Success through `outputs/run_metadata.json`

Open `outputs/run_metadata.json` after running the pipeline.

A successful real SiliconFlow API run should include:

```json
{
  "requested_provider": "siliconflow",
  "provider": "siliconflow",
  "api_reached": true,
  "validation_passed": true,
  "fallback_used": false,
  "error": null
}
```

The verified V3 local run used:

```text
model = deepseek-ai/DeepSeek-V4-Flash
raw_row_count = 1001
processed_customer_count = 1000
```

If `provider` is `mock` while `requested_provider` is `siliconflow`, the system used fallback output. Check `api_reached`, `validation_passed`, and `error` to see whether the cause was API access or validation failure.

## AI Insight Outputs

`data/processed/fact_user_behavior_scored.csv` is the recommended fact table for Power BI main visuals. It contains one row per user with original user fields, RFM scores, weighted AOV, Value Proxy Score, English segment name, Chinese segment name, business role, and action priority.

`outputs/segment_insights.md` contains:

- Project run time
- Data source
- Core customer segment results
- High-value customer insights
- Churn-risk customer insights
- Marketing recommendations
- Human Review reminder
- Structured Summary Used By LLM

`outputs/powerbi_llm_insights.csv` contains Power BI-readable insight rows with:

- `insight_title`
- `insight_text`
- `segment_name`
- `priority`
- `review_status`
- `generated_at`

`outputs/run_metadata.json` records:

- `run_time_utc`
- `raw_files`
- `raw_row_count`
- `processed_customer_count`
- `requested_provider`
- `provider`
- `model`
- `api_reached`
- `validation_passed`
- `fallback_used`
- `error`
- `retry_count`
- `error_type`
- `output_files`

## Power BI Integration

Power BI should use the regenerated CSV outputs from the same V3 pipeline:

- Main BI visuals should read `data/processed/fact_user_behavior_scored.csv`.
- The AI Insight Box should read `outputs/powerbi_llm_insights.csv`.

This keeps the pie charts, bar charts, customer counts, and AI insight text aligned with the same segment logic from one pipeline run.

If Power BI visuals and the AI Insight Box show different segment counts, the usual cause is that the main Power BI visuals are still connected to an old table, such as `Fact_User_Behavior`, or to an old segment field. Repoint those visuals to `data/processed/fact_user_behavior_scored.csv` and use `segment_name` or `segment_name_cn` from that file.

After running the pipeline, open:

```text
powerbi/AI_Customer_Segmentation_Dashboard.pbix
```

Then click **Home -> Refresh** in Power BI Desktop.

The AI-generated recommendations are designed as reviewable insight text, not as automated campaign execution.

## Numeric Validation

Python calculates the business metrics first and passes a structured summary to the LLM. The LLM is instructed to use only those numbers.

Numeric validation checks the LLM response against the structured summary to reduce unsupported business-number hallucination. The validation is designed to:

- Allow section numbering and list numbering.
- Allow reasonable rounding of numbers already present in the structured summary.
- Allow percentage and decimal representations within a small tolerance.
- Focus on business-number contexts such as customers, share, weighted AOV, RFM score, Value Proxy Score, recency, spending, and frequency.
- Reject obvious new business metrics that are not supported by Python-computed results.

This keeps the guardrail practical: it reduces hallucinated business metrics without blocking normal report formatting.

## Fallback Mechanism

The pipeline keeps running even when the API path fails.

Fallback can happen when:

- The API key is missing or invalid.
- The API endpoint cannot be reached.
- The provider returns an invalid response.
- Numeric validation rejects unsupported business numbers.

When fallback is used, `outputs/run_metadata.json` records `fallback_used = true` and stores the error message. This makes the result auditable while preserving a usable Mock output for demos and Power BI refresh.

## Human-in-the-loop Review

AI-generated recommendations are decision-support drafts only. Before any marketing campaign is executed, business users should review:

- Segment definitions and raw data freshness.
- Whether the recommendation matches business reality.
- Campaign eligibility, compliance, and brand tone.
- Inventory, logistics, customer support, and after-sales capacity.
- Whether the final campaign should be approved, revised, or rejected.

## Business Value

This project demonstrates how AI can improve BI decision workflows by:

- Turning static dashboard outputs into decision-ready summaries.
- Reducing repetitive manual reporting work.
- Connecting customer segmentation results with marketing actions.
- Keeping business metrics grounded in Python-computed structured data.
- Making API usage, validation, and fallback status auditable.
- Preserving human responsibility for final business decisions.

## Role Relevance

This project is relevant to AI Solutions Intern, AI Product Intern, AI Pre-sales Intern, Data Analyst, BI Analyst, and Technical Consultant roles.

It demonstrates:

- Data cleaning and customer segmentation workflow design.
- RFM and customer value metric modeling.
- LLM API integration with operational guardrails.
- Power BI integration and refreshable insight outputs.
- Human-in-the-loop AI governance.
- Clear communication of business value and technical implementation.

## V3.4 Eval Harness

V3.4 adds a lightweight evaluation harness for the Router Agent and Orchestrator. It tests intent routing, tool selection, risk classification, dry-run safety, high-risk refusal behavior, and whether answers contain required business keywords.

The eval is deterministic and local. It does not call SiliconFlow, does not switch raw data, does not run the pipeline, and does not modify Power BI files.

Run:

```cmd
.venv\Scripts\python.exe eval\run_eval.py
```

Results are written to:

```text
eval/eval_results.csv
```

## V3.5 Streamlit Agent Workbench

V3.5 adds a lightweight staff-facing Streamlit page on top of the existing Router Agent, Orchestrator, Skill Layer, and Eval Harness.

The UI is Chinese-first for HR/interviewer demos, while keeping technical fields such as `Provider`, `Intent`, `Tools`, `Risk Level`, `Dry Run`, commands, file names, and stable CSV fields in English. The layout uses a clean consulting-style dashboard design: white background, dark navy accents, thin dividers, compact cards, and high information density.

It supports natural-language workflow questions, Chinese RFM summary lookup from `data/processed/customer_segments.csv`, Power BI output preview, eval result preview, and explicit sidebar buttons for applying a demo raw case, running the pipeline, or running the eval harness.

The page defaults to `mock` provider. It does not automatically switch raw data, run the pipeline, or call the real API. Actions that can modify local workflow outputs require a button click.

Run:

```cmd
.venv\Scripts\streamlit.exe run streamlit_agent_app.py
```

## Future Work

The following items are future directions, not completed V3 features:

- RFM Skill Agent
- Safe SQL Skill
- Agentic BI workflow
- Evaluation Harness
- Trace Viewer
