# AI-assisted Customer Segmentation Dashboard V3

V3 upgrades this project into an **AI-assisted BI Decision Workflow with SiliconFlow API**.

After replacing the raw e-commerce CSV files under `data/raw/`, run one pipeline command to regenerate customer segmentation data, AI-assisted marketing insights, Power BI insight CSV, and run metadata.

## What V3 Generates

The main pipeline regenerates:

```text
data/processed/customer_segments.csv
outputs/segment_insights.md
outputs/powerbi_llm_insights.csv
outputs/run_metadata.json
```

For compatibility with the earlier Power BI prototype, the insight Markdown and Power BI CSV are also mirrored to:

```text
llm_agent/outputs/segment_insights.md
llm_agent/outputs/powerbi_llm_insights.csv
```

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
`-- README.md
```

## Pipeline Workflow

```text
data/raw/*.csv
        ->
Python cleaning and RFM/value scoring
        ->
data/processed/customer_segments.csv
        ->
Structured summary
        ->
Mock LLM or SiliconFlow API
        ->
outputs/segment_insights.md
outputs/powerbi_llm_insights.csv
outputs/run_metadata.json
```

The LLM does **not** calculate business metrics. Python calculates the RFM fields, weighted AOV, Value Proxy Score, customer segment distribution, and cross-dimensional findings first. The LLM only turns that structured summary into business-language recommendations.

## Metrics

V3 calculates:

- **Recency**: `Last_Login_Days_Ago`; lower means more recent activity.
- **Frequency**: `Purchase_Frequency` aggregated per customer.
- **Monetary**: `Total_Spending` aggregated per customer.
- **Weighted AOV**: total spending divided by total purchase frequency.
- **RFM Score**: recency, frequency, and monetary scores on a 1-5 scale.
- **Value Proxy Score**: 0-100 percentile score using 45% monetary, 25% frequency, 20% weighted AOV, and 10% recency.
- **Customer Segment**: High-value, Potential, Churn-risk, Regular Retained, or Other Customers.

## Environment Configuration

Copy `.env.example` to `.env` and choose one provider.

### Mock mode

Use this for local portfolio demos and offline testing:

```env
LLM_PROVIDER=mock
```

Mock mode does not call any external API.

### SiliconFlow mode

Use this when you want real API-generated business wording:

```env
LLM_PROVIDER=siliconflow
SILICONFLOW_API_KEY=your_siliconflow_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=Qwen/Qwen2.5-7B-Instruct
```

Do not commit real API keys. `.env` is ignored by Git.

## How to Run on Windows

From Windows cmd:

```cmd
cd /d D:\chatgpt\AI-assisted-Customer-Segmentation-Dashboard
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe run_pipeline.py
```

You can also run the PowerShell helper:

```cmd
cd /d D:\chatgpt\AI-assisted-Customer-Segmentation-Dashboard
powershell -ExecutionPolicy Bypass -File run_pipeline.ps1
```

Optional one-run provider override:

```cmd
.venv\Scripts\python.exe run_pipeline.py --provider mock
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

## How to Replace Raw Data

1. Put the new e-commerce CSV file under `data/raw/`.
2. Keep the expected columns, including `User_ID`, `Last_Login_Days_Ago`, `Purchase_Frequency`, `Total_Spending`, and `Product_Category_Preference`.
3. Run the pipeline again.
4. Check `outputs/run_metadata.json` and confirm `run_time_utc`, `raw_files`, `raw_row_count`, and `processed_customer_count` changed as expected.

The pipeline reads all `*.csv` files under `data/raw/`. If you want to run on only one dataset, keep only that raw CSV in the folder.

## How to Confirm SiliconFlow Was Used

Open `outputs/run_metadata.json`.

Real SiliconFlow success should look like:

```json
{
  "requested_provider": "siliconflow",
  "provider": "siliconflow",
  "api_reached": true,
  "validation_passed": true,
  "model": "Qwen/Qwen2.5-7B-Instruct",
  "fallback_used": false,
  "error": null
}
```

If the API key, network, endpoint, or model fails, the pipeline automatically falls back to Mock:

```json
{
  "requested_provider": "siliconflow",
  "provider": "mock",
  "api_reached": true,
  "validation_passed": false,
  "fallback_used": true,
  "error": "..."
}
```

If the API could not be reached at all, `api_reached` is `false`. If the API returned content but the numeric guardrail rejected unsupported business metrics, `api_reached` is `true` and `validation_passed` is `false`. This keeps the BI workflow runnable while making provider status auditable.

## Output Files

### `data/processed/customer_segments.csv`

Contains segment-level output for Power BI:

- segment
- share
- customer_count
- business_role
- weighted_aov
- avg_recency_days
- avg_rfm_score
- avg_value_proxy_score
- category_preference
- key_issue
- action_priority

### `outputs/segment_insights.md`

Contains:

- Project run time
- Data source
- Core customer segment results
- High-value customer insights
- Churn-risk customer insights
- Marketing recommendations
- Human Review reminder
- Structured Summary Used By LLM

### `outputs/powerbi_llm_insights.csv`

Contains at least:

- insight_title
- insight_text
- segment_name
- priority
- review_status
- generated_at

### `outputs/run_metadata.json`

Contains:

- run_time_utc
- raw_files
- raw_row_count
- processed_customer_count
- requested_provider
- provider
- model
- api_reached
- validation_passed
- fallback_used
- error
- output_files

## Human Review Guardrail

AI-generated recommendations are decision-support drafts only. Before any marketing campaign is executed, a human reviewer must verify segment rules, raw data freshness, campaign eligibility, inventory, logistics, compliance, and brand tone.

## Power BI Refresh

After running the pipeline, open:

```text
powerbi/AI_Customer_Segmentation_Dashboard.pbix
```

Then click **Home -> Refresh** in Power BI Desktop.
