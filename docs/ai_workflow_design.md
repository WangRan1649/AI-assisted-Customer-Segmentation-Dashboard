# AI Workflow Design

## 1. Workflow Objective

The goal of this workflow is to upgrade a traditional Power BI customer segmentation dashboard into an AI-assisted decision intelligence system.

The system is designed to reduce repetitive manual work in three areas:

1. Preparing processed business CSV files.
2. Generating AI-assisted business recommendations.
3. Updating the Power BI LLM Insight Box.

The final workflow allows the user to start from a raw e-commerce user behavior dataset and generate all downstream analytical and AI insight outputs through a one-click local pipeline.

---

## 2. End-to-end Workflow

```text
Raw user behavior dataset
        ↓
Python data preparation
        ↓
Processed customer segment data
        ↓
Python insight generation
        ↓
Mock LLM / replaceable LLM client
        ↓
Markdown business report
        ↓
Power BI-ready insight CSV
        ↓
Power BI Refresh
        ↓
LLM Insight Box
        ↓
Human review
```

---

## 3. Input Layer

### Raw Dataset

The raw dataset is stored at:

```text
data/raw/ecommerce_user_behavior_dataset.csv
```

The raw dataset contains user-level behavior fields, including:

- `User_ID`
- `Age`
- `Gender`
- `Location`
- `Purchase_Frequency`
- `Average_Order_Value`
- `Total_Spending`
- `Product_Category_Preference`
- `Last_Login_Days_Ago`

Current data granularity:

```text
One row = one user-level behavior summary
```

This means the dataset is not an order-level transaction table. It does not contain raw `OrderID` or order-level `Amount` fields.

---

## 4. Data Preparation Layer

The data preparation logic is implemented in:

```text
llm_agent/src/prepare_processed_data.py
```

This script automatically generates:

```text
data/processed/customer_segments.csv
data/processed/cross_dimensional_insights.csv
```

### Main Responsibilities

The script performs the following tasks:

1. Loads the raw user behavior dataset.
2. Cleans invalid or description rows.
3. Converts numeric columns into proper numeric types.
4. Assigns customer segments based on user-level behavior rules.
5. Calculates segment share, weighted AOV, category preference, and business role.
6. Generates cross-dimensional insights such as age-gender value patterns, regional category opportunities, Pareto-style value concentration, and churn recovery signals.

---

## 5. Metric Design

Because the dataset is user-level aggregated data, AOV is calculated as weighted AOV:

```DAX
Weighted AOV =
DIVIDE(
    [Total Spending],
    [Total Purchase Frequency]
)
```

This is more reliable than directly averaging `Average_Order_Value`, because users may have different purchase frequencies.

The project separates three different types of metrics:

| Metric | Meaning | Usage |
|---|---|---|
| Total Spending | Total historical spending | GMV proxy / spending contribution |
| Weighted AOV | Average spending per purchase | Consumption level analysis |
| Customer Value Index | Weighted AOV × Frequency Score | Relative value ranking |

This distinction prevents a scoring metric from being mistakenly treated as a financial amount.

---

## 6. AI Insight Generation Layer

The AI insight generation logic is implemented in:

```text
llm_agent/src/insight_generator.py
```

This script automatically reads:

```text
data/processed/customer_segments.csv
data/processed/cross_dimensional_insights.csv
```

Then it generates:

```text
llm_agent/outputs/segment_insights.md
llm_agent/outputs/powerbi_llm_insights.csv
```

### Output 1: Markdown Report

```text
llm_agent/outputs/segment_insights.md
```

This file is designed for human reading and portfolio explanation. It includes:

- Executive summary
- Segment interpretation
- Priority marketing actions
- Human-in-the-loop review checklist

### Output 2: Power BI Insight CSV

```text
llm_agent/outputs/powerbi_llm_insights.csv
```

This file is designed for Power BI. It contains structured fields:

- `insight_title`
- `insight_text`
- `review_status`

Power BI reads this CSV and displays it as the LLM Insight Box.

---

## 7. LLM Client Layer

The LLM interface is implemented in:

```text
llm_agent/src/llm_client.py
```

The current project uses Mock LLM mode.

### Mock LLM Mode

Mock LLM mode does not call an external API. It returns a stable predefined insight report.

Advantages:

- No API key required
- No cost
- No network dependency
- Stable for interviews and demos
- No risk of exposing secrets on GitHub

### Production LLM Mode

In production, the same `call_llm()` interface can be replaced by:

- OpenAI API
- Gemini API
- Claude API
- Enterprise-hosted LLM API
- Local LLM through Ollama or similar tools

This modular design allows the AI layer to be upgraded without changing the entire pipeline.

---

## 8. One-click Pipeline

The one-click local pipeline is implemented in:

```text
run_pipeline.ps1
```

Run it from the project root:

```powershell
.\run_pipeline.ps1
```

The script performs:

1. Dependency check / installation.
2. Raw data processing.
3. Processed CSV generation.
4. AI insight report generation.
5. Power BI CSV generation.

After running the pipeline, the user only needs to open Power BI and click:

```text
Home -> Refresh
```

---

## 9. Human-in-the-loop Design

This project does not allow AI to directly execute customer-facing campaigns.

The AI layer only generates draft recommendations. Before execution, human reviewers must check:

1. Whether the customer segment definition is correct.
2. Whether the input data is reliable.
3. Whether the recommendation is supported by the data.
4. Whether the marketing message is appropriate.
5. Whether logistics, after-sales, and inventory capacity can support the action.

This ensures that AI accelerates decision preparation but does not replace business accountability.

---

## 10. Reusable Workflow Template

This workflow can be reused in other business scenarios:

```text
Raw business data
        ↓
Python data preparation
        ↓
Processed analytical tables
        ↓
BI dashboard
        ↓
LLM insight generation
        ↓
Structured recommendation output
        ↓
Human review
```

Potential reusable scenarios include:

- Customer churn analysis
- Sales lead scoring
- Course operation analysis
- Cross-border e-commerce review analysis
- SaaS customer health scoring
- Marketing campaign performance diagnosis