from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "llm_agent" / "src"
OUTPUT_DIR = ROOT_DIR / "outputs"
METADATA_FILE = OUTPUT_DIR / "run_metadata.json"

sys.path.insert(0, str(SRC_DIR))

from insight_generator import generate_outputs  # noqa: E402
from prepare_processed_data import build_structured_summary, run_processing, utc_now_iso  # noqa: E402


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT_DIR)).replace("\\", "/")


def build_metadata(
    structured_summary: dict[str, Any],
    insight_result: Any,
    processed_output_files: dict[str, Path],
) -> dict[str, Any]:
    output_files = {
        **{name: relative_path(path) for name, path in processed_output_files.items()},
        **{
            name: relative_path(path)
            for name, path in insight_result.output_files.items()
            if not name.startswith("legacy_")
        },
        "run_metadata": relative_path(METADATA_FILE),
    }

    llm_response = insight_result.llm_response

    return {
        "run_time_utc": structured_summary.get("run_time_utc"),
        "raw_files": structured_summary.get("data_sources", []),
        "raw_row_count": structured_summary.get("raw_row_count"),
        "cleaned_row_count": structured_summary.get("cleaned_row_count"),
        "processed_customer_count": structured_summary.get("processed_customer_count"),
        "requested_provider": llm_response.requested_provider,
        "provider": llm_response.provider,
        "model": llm_response.model,
        "api_reached": llm_response.api_reached,
        "validation_passed": llm_response.validation_passed,
        "fallback_used": llm_response.fallback_used,
        "error": llm_response.error,
        "retry_count": llm_response.retry_count,
        "error_type": llm_response.error_type,
        "output_files": output_files,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the V3 AI-assisted BI decision workflow pipeline."
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
    run_time_utc = utc_now_iso()

    print("== V3 AI-assisted BI Decision Workflow ==")
    print("Step 1/3: processing raw data from data/raw...")
    processed = run_processing()

    print("Step 2/3: building structured summary and LLM insights...")
    structured_summary = build_structured_summary(processed, run_time_utc=run_time_utc)
    insight_result = generate_outputs(structured_summary, provider=args.provider)

    print("Step 3/3: writing run metadata...")
    metadata = build_metadata(
        structured_summary=structured_summary,
        insight_result=insight_result,
        processed_output_files=processed.output_files,
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

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
    print("Generated V3 files:")
    print(f"- {relative_path(processed.output_files['fact_user_behavior_scored'])}")
    print(f"- {relative_path(processed.output_files['customer_segments'])}")
    print(f"- {relative_path(insight_result.output_files['segment_insights'])}")
    print(f"- {relative_path(insight_result.output_files['powerbi_llm_insights'])}")
    print(f"- {relative_path(METADATA_FILE)}")


if __name__ == "__main__":
    main()
