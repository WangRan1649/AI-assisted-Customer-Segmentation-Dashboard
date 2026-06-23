# V3.3 Lightweight Router Agent / Orchestrator

## Positioning

V3.3 adds a lightweight Agent orchestration layer on top of the V3.2 Skill Layer.

It is intentionally small and deterministic. It does not introduce LangChain, LangGraph, FastAPI, Docker, databases, or any large runtime dependency. The goal is to demonstrate how an AI BI workflow can be prepared for future agentic orchestration while keeping the current pipeline stable, auditable, and easy to run locally.

## Architecture

```text
User question
    ->
Router Agent
    ->
AgentPlan
    ->
Orchestrator Agent
    ->
Deterministic Skills / Whitelisted local actions
    ->
Trace Logger
```

## Component Responsibilities

### Router Agent

The Router Agent is deterministic and does not call an LLM.

It classifies user questions into:

- `list_demo_cases`
- `compare_demo_cases`
- `workflow_status`
- `run_workflow`
- `explain_powerbi_workflow`
- `unknown`

It also assigns a risk level:

- Read-only questions are `low` risk.
- Workflow execution plans are `medium` risk.
- Deletion, reset, clearing, or unsafe overwrite requests are refused or marked as high risk.

The Router Agent does not calculate metrics, modify files, or call the LLM.

### Orchestrator Agent

The Orchestrator Agent executes the plan selected by the Router.

Read-only capabilities include:

- Listing demo cases under `data/demo_cases`.
- Comparing `baseline_original` and `apparel_vip_shift` customer segment summaries.
- Reading `outputs/run_metadata.json` to summarize the latest workflow state.
- Explaining how Power BI uses the scored fact table and AI insight table.

Execution is dry-run by default. For workflow execution, the Orchestrator only allows whitelisted local actions:

- `scripts/apply_raw_case.py <case_name>`
- `run_pipeline.py --provider mock`

It does not execute arbitrary shell commands and does not access paths outside the project root.

### Skill Layer

The Skill Layer remains responsible for deterministic business work:

- Data quality checks
- RFM segmentation
- User-level scored fact table generation
- Structured summary generation
- LLM or Mock insight generation
- Numeric validation
- Fallback
- Power BI export checks

The Agent layer does not replace these Skills. It only chooses and sequences them.

### Trace Logger

Each Agent run writes one JSON line to:

```text
logs/agent_runs.jsonl
```

Each trace record includes:

- `run_id`
- `timestamp`
- `question`
- `intent`
- `selected_tools`
- `dry_run`
- `status`
- `error`

This makes the lightweight Agent layer observable without adding an external tracing platform.

## Mock and API Workflow

The existing V3 pipeline still supports both Mock mode and SiliconFlow API mode.

The Agent execution path is intentionally conservative:

- Read-only Agent questions never call the LLM.
- Dry-run workflow questions only show the planned commands.
- The current executable Agent workflow only runs `run_pipeline.py --provider mock`.

SiliconFlow API mode remains available through the normal pipeline command:

```cmd
.venv\Scripts\python.exe run_pipeline.py --provider siliconflow
```

This separation keeps demo orchestration safe while preserving the verified SiliconFlow path for direct pipeline runs.

## Why Not LangChain or LangGraph Yet

V3.3 does not need a full agent framework because the current problem is small and well-bounded:

- Intent routing is deterministic.
- Tools are local and limited.
- The workflow has strict file contracts.
- RFM logic and numeric validation should remain controlled Python code.
- The main requirement is traceable orchestration, not open-ended planning.

Avoiding a large framework keeps the project easier to inspect in interviews and prevents unnecessary runtime complexity.

## Example Commands

```cmd
.venv\Scripts\python.exe run_agent.py --question "列出可用数据场景"
.venv\Scripts\python.exe run_agent.py --question "对比 baseline_original 和 apparel_vip_shift 的分群变化"
.venv\Scripts\python.exe run_agent.py --question "如果我要切换到 apparel_vip_shift 并刷新 Power BI，需要执行什么"
.venv\Scripts\python.exe run_agent.py --question "切换到 apparel_vip_shift 并运行 workflow" --execute --provider mock
```

By default, `run_agent.py` uses dry-run mode and does not switch raw data or run the pipeline.
