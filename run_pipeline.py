from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skills.workflow_skill import run_ai_bi_workflow


ROOT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the V3.2 AI-assisted BI skill-layer workflow."
    )
    parser.add_argument(
        "--provider",
        choices=["mock", "siliconflow"],
        default=None,
        help="Override LLM_PROVIDER from .env for this run.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("== V3.2 AI-assisted BI Skill Workflow ==")
    print("Step 1/4: checking raw data quality...")
    print("Step 2/4: running deterministic RFM segmentation skill...")
    print("Step 3/4: running insight generation skill...")
    print("Step 4/4: validating Power BI export files...")

    workflow_result = run_ai_bi_workflow(provider=args.provider)
    if workflow_result.get("status") == "error":
        print("")
        print("Pipeline failed.")
        print(workflow_result)
        sys.exit(1)

    metadata = workflow_result["metadata"]

    print("")
    print("Pipeline completed.")
    print(f"Requested provider: {metadata['requested_provider']}")
    print(f"Actual provider: {metadata['provider']}")
    print(f"Model: {metadata['model']}")
    print(f"API reached: {metadata['api_reached']}")
    print(f"Validation passed: {metadata['validation_passed']}")
    print(f"Fallback used: {metadata['fallback_used']}")
    print(f"Retry count: {metadata['retry_count']}")
    print(f"Error type: {metadata['error_type']}")
    if metadata["error"]:
        print(f"Provider error: {metadata['error']}")

    print("")
    print("Generated files:")
    output_files = metadata["output_files"]
    for key in [
        "fact_user_behavior_scored",
        "customer_segments",
        "cross_dimensional_insights",
        "segment_insights",
        "powerbi_llm_insights",
        "run_metadata",
    ]:
        if key in output_files:
            print(f"- {output_files[key]}")


if __name__ == "__main__":
    main()
