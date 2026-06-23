from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from skills import ROOT_DIR, ensure_src_path, relative_path
from skills.data_quality_skill import inspect_raw_data
from skills.insight_generation_skill import run_insight_generation
from skills.powerbi_export_skill import validate_powerbi_exports
from skills.rfm_segmentation_skill import run_rfm_segmentation


ensure_src_path()

from prepare_processed_data import utc_now_iso  # noqa: E402


OUTPUT_DIR = ROOT_DIR / "outputs"
METADATA_FILE = OUTPUT_DIR / "run_metadata.json"


def _build_metadata(
    structured_summary: dict[str, Any],
    insight_result: Any,
    processed_output_files: dict[str, Path],
) -> dict[str, Any]:
    llm_response = insight_result.llm_response
    output_files = {
        **{name: relative_path(path) for name, path in processed_output_files.items()},
        **{
            name: relative_path(path)
            for name, path in insight_result.output_files.items()
            if not name.startswith("legacy_")
        },
        "run_metadata": relative_path(METADATA_FILE),
    }

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


def _without_internal_keys(result: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in result.items()
        if not key.startswith("_")
    }


def run_ai_bi_workflow(provider: str = "mock") -> dict[str, Any]:
    run_time_utc = utc_now_iso()

    data_quality_result = inspect_raw_data()
    rfm_result = run_rfm_segmentation(include_processed_result=True)
    if rfm_result.get("status") == "error":
        return {
            "status": "error",
            "run_time_utc": run_time_utc,
            "data_quality": data_quality_result,
            "rfm_segmentation": _without_internal_keys(rfm_result),
        }

    processed_result = rfm_result["_processed_result"]
    insight_result = run_insight_generation(
        processed_result=processed_result,
        provider=provider,
        run_time_utc=run_time_utc,
        include_artifacts=True,
    )
    if insight_result.get("status") == "error":
        return {
            "status": "error",
            "run_time_utc": run_time_utc,
            "data_quality": data_quality_result,
            "rfm_segmentation": _without_internal_keys(rfm_result),
            "insight_generation": _without_internal_keys(insight_result),
        }

    structured_summary = insight_result["_structured_summary"]
    raw_insight_result = insight_result["_insight_result"]
    metadata = _build_metadata(
        structured_summary=structured_summary,
        insight_result=raw_insight_result,
        processed_output_files=processed_result.output_files,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    powerbi_export_result = validate_powerbi_exports()

    return {
        "status": "ok" if powerbi_export_result.get("status") == "ok" else "warning",
        "run_time_utc": run_time_utc,
        "data_quality": data_quality_result,
        "rfm_segmentation": _without_internal_keys(rfm_result),
        "insight_generation": _without_internal_keys(insight_result),
        "powerbi_export": powerbi_export_result,
        "metadata": metadata,
        "output_files": metadata["output_files"],
    }
