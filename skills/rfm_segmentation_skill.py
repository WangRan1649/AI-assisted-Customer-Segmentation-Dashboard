from __future__ import annotations

from pathlib import Path
from typing import Any

from skills import ensure_src_path, relative_path


ensure_src_path()

from prepare_processed_data import RAW_DIR, ProcessedDataResult, run_processing  # noqa: E402


def run_rfm_segmentation(
    raw_dir: Path = RAW_DIR,
    include_processed_result: bool = False,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "ok",
        "segment_count": {},
        "processed_customer_count": 0,
        "output_paths": {},
    }

    try:
        processed: ProcessedDataResult = run_processing(raw_dir=raw_dir)
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        return result

    result["segment_count"] = {
        str(row["segment"]): int(row["customer_count"])
        for row in processed.customer_segments[["segment", "customer_count"]].to_dict(orient="records")
    }
    result["processed_customer_count"] = int(processed.processed_customer_count)
    result["output_paths"] = {
        name: relative_path(path)
        for name, path in processed.output_files.items()
    }

    if include_processed_result:
        result["_processed_result"] = processed

    return result
