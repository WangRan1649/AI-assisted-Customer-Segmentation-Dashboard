from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
FACT_USER_BEHAVIOR_SCORED_FILE = ROOT_DIR / "data" / "processed" / "fact_user_behavior_scored.csv"
SEGMENT_FILE = ROOT_DIR / "data" / "processed" / "customer_segments.csv"
POWERBI_INSIGHT_FILE = ROOT_DIR / "outputs" / "powerbi_llm_insights.csv"


def load_fact_user_behavior_scored(path: Path = FACT_USER_BEHAVIOR_SCORED_FILE) -> pd.DataFrame:
    return pd.read_csv(path)


def load_customer_segments(path: Path = SEGMENT_FILE) -> pd.DataFrame:
    return pd.read_csv(path)


def load_powerbi_insights(path: Path = POWERBI_INSIGHT_FILE) -> pd.DataFrame:
    return pd.read_csv(path)
