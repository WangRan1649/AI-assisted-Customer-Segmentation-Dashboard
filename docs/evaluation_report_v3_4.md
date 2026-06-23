# V3.4 Eval Harness Report

## Purpose

V3.4 adds a lightweight Eval Harness for the Router Agent, Orchestrator, and Skill workflow boundaries.

The purpose is to show that the agent layer is not just working by accident. It can be tested systematically with repeatable cases, expected intents, expected tools, expected risk levels, dry-run behavior, refusal behavior, and required answer keywords.

## What Is Tested

The eval dataset covers:

- Router intent recognition
- Tool selection
- Risk level classification
- Dry-run safety boundary
- High-risk request refusal
- Whether the final answer contains key business information

The eval intentionally uses dry-run mode. It does not switch raw data, does not run the pipeline, does not call SiliconFlow, and does not modify Power BI files.

## Current Dataset

Dataset path:

```text
eval/eval_dataset.csv
```

Current coverage includes:

- `list_demo_cases`
- `compare_demo_cases`
- `workflow_status`
- `explain_powerbi_workflow`
- `run_workflow` dry-run
- high-risk delete/reset requests
- unknown questions

The dataset currently contains 14 cases, mostly Chinese questions with a few English examples.

## Current Eval Summary

Latest local run:

```text
Total cases: 14
Intent accuracy: 100.0%
Tool selection accuracy: 100.0%
Risk level accuracy: 100.0%
Dry-run accuracy: 100.0%
Refusal accuracy: 100.0%
Answer contains accuracy: 100.0%
Overall pass rate: 100.0%
```

Results are written to:

```text
eval/eval_results.csv
```

## Why Real LLM API Is Not Tested Here

This eval harness does not test the real SiliconFlow API path because API behavior depends on network latency, service availability, model-side timing, and credentials.

The real LLM path remains protected in the pipeline layer by:

- Numeric validation
- Retry and timeout handling
- Mock fallback
- Provider and validation metadata in `outputs/run_metadata.json`

V3.4 focuses on deterministic local agent behavior: routing, orchestration, dry-run safety, refusal safety, and answer contracts.

## Safety Boundary

The eval confirms that:

- Read-only requests stay read-only.
- `run_workflow` requests are dry-run by default.
- Unsafe delete/reset/clear/overwrite style requests are refused or marked high risk.
- The Orchestrator does not execute arbitrary shell commands.
- The Orchestrator does not access paths outside the project root.

## How to Run

```cmd
.venv\Scripts\python.exe eval\run_eval.py
```

Compile check:

```cmd
.venv\Scripts\python.exe -c "import py_compile, glob; [py_compile.compile(p, doraise=True) for p in ['eval/run_eval.py','eval/metrics.py'] + glob.glob('agents/*.py')]; print('py_compile ok')"
```

## Future Eval Extensions

The next evaluation layers can include:

- SQL sandbox eval
- Numeric hallucination eval
- Fallback simulation eval
- Power BI output schema eval
