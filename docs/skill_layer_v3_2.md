# V3.2 Skill Layer Design

## Purpose

V3.2 keeps the existing V3.1 pipeline stable and introduces a thin deterministic Skill layer around it. This is not a rewrite into a complex agent system. The goal is to make each reliable pipeline capability callable by a future agent without changing the current CSV outputs, Power BI refresh flow, RFM segmentation rules, numeric validation, or fallback behavior.

## Design Principle

The LLM does not calculate business metrics.

Python Skills handle deterministic work:

- Raw data checks
- RFM and customer segmentation
- Structured summary generation
- Mock or SiliconFlow insight generation
- Numeric validation and fallback
- Power BI export checks

A future Agent should only select and orchestrate Skills. It should not directly calculate RFM, change segment rules, inspect user-level raw records in the prompt, or invent business numbers.

## Skill Modules

```text
skills/
|-- __init__.py
|-- data_quality_skill.py
|-- rfm_segmentation_skill.py
|-- insight_generation_skill.py
|-- powerbi_export_skill.py
`-- workflow_skill.py
```

### `data_quality_skill.py`

Checks raw CSV files under `data/raw/`.

Responsibilities:

- Read raw files with the existing encoding fallback.
- Check required columns.
- Identify business rows using the same source fields used by the pipeline.
- Return row counts, missing columns, and status.

### `rfm_segmentation_skill.py`

Wraps the existing deterministic processing function.

Responsibilities:

- Reuse the current RFM and customer segmentation logic.
- Preserve the existing segment definitions and metric formulas.
- Regenerate:
  - `data/processed/fact_user_behavior_scored.csv`
  - `data/processed/customer_segments.csv`
  - `data/processed/cross_dimensional_insights.csv`
- Return segment counts and output paths.

### `insight_generation_skill.py`

Wraps the existing LLM insight generation path.

Responsibilities:

- Build the structured summary from aggregated Python outputs.
- Keep Mock and SiliconFlow modes.
- Keep numeric validation, retry, and fallback behavior.
- Ensure the LLM receives only aggregate structured summary content, not the 1,000-row user-level fact table.
- Return provider, API reachability, validation status, fallback status, retry count, and error type.

### `powerbi_export_skill.py`

Checks that Power BI-facing files exist and are readable.

Responsibilities:

- Validate:
  - `data/processed/fact_user_behavior_scored.csv`
  - `data/processed/customer_segments.csv`
  - `outputs/powerbi_llm_insights.csv`
- Return row counts, columns, and status.

### `workflow_skill.py`

Provides the top-level callable:

```python
run_ai_bi_workflow(provider: str = "mock") -> dict
```

It calls Skills in order:

1. Data quality check
2. RFM segmentation
3. Insight generation
4. Power BI export validation

It also writes `outputs/run_metadata.json` in the existing compatible format so Power BI refresh behavior is not broken.

## Why This Helps Future Agent Work

The Skill layer creates a clear boundary between deterministic computation and agent orchestration.

Future Agent work can focus on:

- Selecting which Skill to run
- Comparing demo cases
- Explaining metadata and validation results
- Producing trace summaries
- Running evaluation scenarios

The Agent should not own:

- RFM math
- Segment assignment logic
- CSV schema contracts
- Numeric validation rules
- Fallback mechanics

## Trace, Eval, Sandbox, and Orchestration

V3.2 makes future improvements easier without adding heavy dependencies now:

- **Trace**: each Skill returns a structured dict, which can be logged later.
- **Eval**: demo cases can compare Skill outputs deterministically.
- **Sandbox**: user-level data can stay inside Python outputs and out of LLM prompts.
- **Agent Orchestration**: a future agent can call `run_ai_bi_workflow()` or individual Skills without knowing internal implementation details.

## Non-goals

V3.2 intentionally does not add:

- LangChain
- LangGraph
- FastAPI
- Docker
- Databases
- Multi-agent runtime
- New RFM logic
- New Power BI schema

The result is a stable, minimal Skill layer on top of the existing V3.1 pipeline.
