from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from skills import ensure_src_path, relative_path


ensure_src_path()

from prepare_processed_data import RAW_DIR, REQUIRED_COLUMNS, read_csv_with_fallback  # noqa: E402


BUSINESS_NUMERIC_COLUMNS = [
    "Last_Login_Days_Ago",
    "Purchase_Frequency",
    "Total_Spending",
]


def _business_row_count(df: pd.DataFrame) -> int:
    working = df.copy()
    working.columns = [str(column).strip() for column in working.columns]

    missing = [column for column in BUSINESS_NUMERIC_COLUMNS if column not in working.columns]
    if "User_ID" not in working.columns or missing:
        return 0

    for column in BUSINESS_NUMERIC_COLUMNS:
        working[column] = pd.to_numeric(working[column], errors="coerce")

    mask = working["User_ID"].astype(str).str.strip().ne("")
    mask &= working[BUSINESS_NUMERIC_COLUMNS].notna().all(axis=1)
    mask &= working["Purchase_Frequency"] >= 0
    mask &= working["Total_Spending"] >= 0

    return int(mask.sum())


def inspect_raw_data(raw_dir: Path = RAW_DIR) -> dict[str, Any]:
    raw_files = sorted(raw_dir.glob("*.csv"))
    result: dict[str, Any] = {
        "raw_path": [relative_path(path) for path in raw_files],
        "total_rows": 0,
        "business_rows": 0,
        "required_columns_present": False,
        "missing_columns": [],
        "files": [],
        "status": "ok",
    }

    if not raw_files:
        result["status"] = "error"
        result["missing_columns"] = list(REQUIRED_COLUMNS)
        return result

    missing_columns: set[str] = set()

    try:
        for raw_file in raw_files:
            df, encoding = read_csv_with_fallback(raw_file)
            df.columns = [str(column).strip() for column in df.columns]
            file_missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
            file_business_rows = 0 if file_missing else _business_row_count(df)

            result["total_rows"] += int(len(df))
            result["business_rows"] += file_business_rows
            missing_columns.update(file_missing)
            result["files"].append(
                {
                    "raw_path": relative_path(raw_file),
                    "encoding": encoding,
                    "total_rows": int(len(df)),
                    "business_rows": file_business_rows,
                    "required_columns_present": not file_missing,
                    "missing_columns": file_missing,
                }
            )
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        return result

    result["missing_columns"] = sorted(missing_columns)
    result["required_columns_present"] = not result["missing_columns"]
    if result["missing_columns"] or result["business_rows"] == 0:
        result["status"] = "error"

    return result
