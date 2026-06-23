from __future__ import annotations

from typing import Any

from skills import ensure_src_path, relative_path


ensure_src_path()

from insight_generator import InsightGenerationResult, build_prompt, generate_outputs  # noqa: E402
from prepare_processed_data import ProcessedDataResult, build_structured_summary  # noqa: E402


def run_insight_generation(
    processed_result: ProcessedDataResult,
    provider: str = "mock",
    run_time_utc: str | None = None,
    include_artifacts: bool = False,
) -> dict[str, Any]:
    structured_summary = build_structured_summary(processed_result, run_time_utc=run_time_utc)
    prompt = build_prompt(structured_summary)

    result: dict[str, Any] = {
        "status": "ok",
        "provider": None,
        "requested_provider": provider,
        "api_reached": False,
        "validation_passed": False,
        "fallback_used": False,
        "retry_count": 0,
        "error_type": None,
        "error": None,
        "prompt_contains_user_level_detail": any(
            token in prompt
            for token in [
                "fact_user_behavior_scored",
                "User_ID",
                "Newsletter_Subscription",
                "segment_name_cn",
            ]
        ),
        "output_paths": {},
    }

    try:
        insight_result: InsightGenerationResult = generate_outputs(
            structured_summary,
            provider=provider,
        )
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        return result

    llm_response = insight_result.llm_response
    result.update(
        {
            "provider": llm_response.provider,
            "requested_provider": llm_response.requested_provider,
            "model": llm_response.model,
            "api_reached": llm_response.api_reached,
            "validation_passed": llm_response.validation_passed,
            "fallback_used": llm_response.fallback_used,
            "retry_count": llm_response.retry_count,
            "error_type": llm_response.error_type,
            "error": llm_response.error,
            "output_paths": {
                name: relative_path(path)
                for name, path in insight_result.output_files.items()
                if not name.startswith("legacy_")
            },
        }
    )

    if result["prompt_contains_user_level_detail"]:
        result["status"] = "warning"

    if include_artifacts:
        result["_structured_summary"] = structured_summary
        result["_insight_result"] = insight_result

    return result
