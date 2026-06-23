from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from skills import ROOT_DIR, relative_path


POWERBI_EXPORT_FILES = {
    "fact_user_behavior_scored": ROOT_DIR / "data" / "processed" / "fact_user_behavior_scored.csv",
    "customer_segments": ROOT_DIR / "data" / "processed" / "customer_segments.csv",
    "powerbi_llm_insights": ROOT_DIR / "outputs" / "powerbi_llm_insights.csv",
}


def validate_powerbi_exports() -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "ok",
        "files": {},
    }

    for name, path in POWERBI_EXPORT_FILES.items():
        file_result: dict[str, Any] = {
            "path": relative_path(path),
            "exists": path.exists(),
            "row_count": 0,
            "columns": [],
            "status": "ok",
        }

        if not path.exists():
            file_result["status"] = "missing"
            result["status"] = "error"
            result["files"][name] = file_result
            continue

        try:
            df = pd.read_csv(path)
            file_result["row_count"] = int(len(df))
            file_result["columns"] = list(df.columns)
        except Exception as exc:
            file_result["status"] = "error"
            file_result["error"] = str(exc)
            result["status"] = "error"

        result["files"][name] = file_result

    return result
