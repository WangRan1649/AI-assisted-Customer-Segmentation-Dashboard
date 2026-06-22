from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
SEGMENT_FILE = ROOT_DIR / "data" / "processed" / "customer_segments.csv"
POWERBI_INSIGHT_FILE = ROOT_DIR / "outputs" / "powerbi_llm_insights.csv"


def load_customer_segments(path: Path = SEGMENT_FILE) -> pd.DataFrame:
    return pd.read_csv(path)


def load_powerbi_insights(path: Path = POWERBI_INSIGHT_FILE) -> pd.DataFrame:
    return pd.read_csv(path)
