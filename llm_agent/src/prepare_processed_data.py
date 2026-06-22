from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

CUSTOMER_SEGMENTS_FILE = PROCESSED_DIR / "customer_segments.csv"
CROSS_INSIGHTS_FILE = PROCESSED_DIR / "cross_dimensional_insights.csv"
FACT_USER_BEHAVIOR_SCORED_FILE = PROCESSED_DIR / "fact_user_behavior_scored.csv"

REQUIRED_COLUMNS = [
    "User_ID",
    "Age",
    "Gender",
    "Location",
    "Income",
    "Last_Login_Days_Ago",
    "Purchase_Frequency",
    "Average_Order_Value",
    "Total_Spending",
    "Product_Category_Preference",
    "Time_Spent_on_Site_Minutes",
    "Pages_Viewed",
]

NUMERIC_COLUMNS = [
    "Age",
    "Income",
    "Last_Login_Days_Ago",
    "Purchase_Frequency",
    "Average_Order_Value",
    "Total_Spending",
    "Time_Spent_on_Site_Minutes",
    "Pages_Viewed",
]

TEXT_COLUMNS = [
    "User_ID",
    "Gender",
    "Location",
    "Interests",
    "Product_Category_Preference",
    "Newsletter_Subscription",
]

SEGMENT_ORDER = [
    "High-value Customers",
    "Potential Customers",
    "Churn-risk Customers",
    "Regular Retained Customers",
    "Other Customers",
]

SEGMENT_CN_MAPPING = {
    "High-value Customers": "高价值用户",
    "Potential Customers": "潜力用户",
    "Churn-risk Customers": "流失风险用户",
    "Regular Retained Customers": "一般保持用户",
    "Other Customers": "其他用户",
}

ROLE_MAPPING = {
    "High-value Customers": "Core profit engine",
    "Potential Customers": "Growth engine",
    "Churn-risk Customers": "Dormant premium assets",
    "Regular Retained Customers": "Traffic foundation",
    "Other Customers": "Long-tail users",
}

ISSUE_MAPPING = {
    "High-value Customers": "Need loyalty protection and VIP retention",
    "Potential Customers": "Large base but low repurchase frequency",
    "Churn-risk Customers": "High historical spending but low recent engagement",
    "Regular Retained Customers": "Frequent buyers with relatively lower spending",
    "Other Customers": "Low engagement and limited short-term value",
}

PRIORITY_MAPPING = {
    "High-value Customers": "Stabilize",
    "Potential Customers": "Convert",
    "Churn-risk Customers": "Recover",
    "Regular Retained Customers": "Upsell",
    "Other Customers": "Nurture",
}


@dataclass(frozen=True)
class RawFileStat:
    path: Path
    row_count: int
    cleaned_row_count: int
    encoding: str

    def to_metadata(self) -> dict[str, Any]:
        return {
            "path": str(self.path.relative_to(ROOT_DIR)).replace("\\", "/"),
            "row_count": self.row_count,
            "cleaned_row_count": self.cleaned_row_count,
            "encoding": self.encoding,
        }


@dataclass
class ProcessedDataResult:
    raw_files: list[RawFileStat]
    raw_row_count: int
    cleaned_row_count: int
    processed_customer_count: int
    customer_level_data: pd.DataFrame
    fact_user_behavior_scored: pd.DataFrame
    customer_segments: pd.DataFrame
    cross_dimensional_insights: pd.DataFrame
    output_files: dict[str, Path]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_with_fallback(path: Path) -> tuple[pd.DataFrame, str]:
    """Read a raw CSV with common encodings used by exported e-commerce data."""

    encodings = ["utf-8-sig", "utf-8", "gbk", "gb18030", "latin1"]
    last_error: Exception | None = None

    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding), encoding
        except UnicodeDecodeError as exc:
            last_error = exc

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"Unable to read {path} with supported encodings: {encodings}. Last error: {last_error}",
    )


def discover_raw_files(raw_dir: Path = RAW_DIR) -> list[Path]:
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {raw_dir}. Put raw e-commerce CSV files there.")
    return files


def validate_columns(df: pd.DataFrame, source: Path) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(
            f"{source} is missing required columns: {', '.join(missing)}. "
            "Please keep the raw e-commerce export schema or update the mapping in prepare_processed_data.py."
        )


def clean_raw_frame(df: pd.DataFrame, source: Path) -> pd.DataFrame:
    """Clean one raw file and remove non-data rows such as field-description rows."""

    df = df.copy()
    df.columns = [str(column).strip() for column in df.columns]
    validate_columns(df, source)

    for column in TEXT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    required_numeric = [
        "Last_Login_Days_Ago",
        "Purchase_Frequency",
        "Total_Spending",
    ]

    df = df.dropna(subset=["User_ID", *required_numeric]).copy()
    df = df[df["User_ID"].astype(str).str.strip().ne("")]
    df = df[df["Purchase_Frequency"] >= 0]
    df = df[df["Total_Spending"] >= 0]
    df["source_file"] = source.name

    return df


def load_raw_data(raw_dir: Path = RAW_DIR) -> tuple[pd.DataFrame, list[RawFileStat]]:
    frames: list[pd.DataFrame] = []
    stats: list[RawFileStat] = []

    for raw_file in discover_raw_files(raw_dir):
        raw_df, encoding = read_csv_with_fallback(raw_file)
        cleaned_df = clean_raw_frame(raw_df, raw_file)
        frames.append(cleaned_df)
        stats.append(
            RawFileStat(
                path=raw_file,
                row_count=len(raw_df),
                cleaned_row_count=len(cleaned_df),
                encoding=encoding,
            )
        )

    return pd.concat(frames, ignore_index=True), stats


def first_non_null(series: pd.Series) -> Any:
    values = series.dropna()
    if values.empty:
        return None
    return values.iloc[0]


def most_common(series: pd.Series) -> Any:
    values = series.dropna()
    if values.empty:
        return None
    return values.mode().iloc[0]


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0 or pd.isna(denominator):
        return 0.0
    return float(numerator) / float(denominator)


def percentile_score(series: pd.Series, higher_is_better: bool) -> pd.Series:
    """Return 1-5 RFM scores, with 5 always meaning better business value."""

    if series.nunique(dropna=True) <= 1:
        return pd.Series([3] * len(series), index=series.index)

    rank_pct = series.rank(method="average", pct=True, ascending=True)
    raw_score = (rank_pct * 5).apply(lambda value: max(1, min(5, int(round(value + 0.499)))))

    if higher_is_better:
        return raw_score.astype(int)

    return (6 - raw_score).clip(lower=1, upper=5).astype(int)


def percentile_value(series: pd.Series, higher_is_better: bool) -> pd.Series:
    if series.nunique(dropna=True) <= 1:
        return pd.Series([0.5] * len(series), index=series.index)

    rank_pct = series.rank(method="average", pct=True, ascending=True)
    if higher_is_better:
        return rank_pct
    return 1 - rank_pct


def build_customer_level_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create one row per customer and calculate RFM plus value proxy metrics."""

    customer_df = (
        df.groupby("User_ID", as_index=False)
        .agg(
            age=("Age", "mean"),
            gender=("Gender", most_common),
            location=("Location", most_common),
            income=("Income", "mean"),
            interests=("Interests", most_common),
            recency_days=("Last_Login_Days_Ago", "min"),
            frequency=("Purchase_Frequency", "sum"),
            average_order_value=("Average_Order_Value", "mean"),
            monetary=("Total_Spending", "sum"),
            category_preference=("Product_Category_Preference", most_common),
            time_spent_minutes=("Time_Spent_on_Site_Minutes", "sum"),
            pages_viewed=("Pages_Viewed", "sum"),
            newsletter_subscription=("Newsletter_Subscription", most_common),
            source_file=("source_file", first_non_null),
        )
    )

    customer_df["weighted_aov"] = customer_df.apply(
        lambda row: safe_divide(row["monetary"], row["frequency"]),
        axis=1,
    )

    customer_df["recency_score"] = percentile_score(customer_df["recency_days"], higher_is_better=False)
    customer_df["frequency_score"] = percentile_score(customer_df["frequency"], higher_is_better=True)
    customer_df["monetary_score"] = percentile_score(customer_df["monetary"], higher_is_better=True)
    customer_df["rfm_score"] = (
        customer_df["recency_score"]
        + customer_df["frequency_score"]
        + customer_df["monetary_score"]
    )

    monetary_pct = percentile_value(customer_df["monetary"], higher_is_better=True)
    frequency_pct = percentile_value(customer_df["frequency"], higher_is_better=True)
    aov_pct = percentile_value(customer_df["weighted_aov"], higher_is_better=True)
    recency_pct = percentile_value(customer_df["recency_days"], higher_is_better=False)

    customer_df["value_proxy_score"] = (
        100
        * (
            monetary_pct * 0.45
            + frequency_pct * 0.25
            + aov_pct * 0.20
            + recency_pct * 0.10
        )
    ).round(2)

    customer_df["customer_segment"] = customer_df.apply(assign_customer_segment, axis=1)

    return customer_df


def assign_customer_segment(row: pd.Series) -> str:
    recency = row["recency_days"]
    frequency = row["frequency"]
    monetary = row["monetary"]
    rfm_score = row["rfm_score"]

    if recency >= 20 and monetary >= 2500:
        return "Churn-risk Customers"
    if rfm_score >= 12 and frequency >= 5 and monetary >= 2500:
        return "High-value Customers"
    if frequency <= 4 and monetary >= 1000:
        return "Potential Customers"
    if frequency >= 5:
        return "Regular Retained Customers"
    return "Other Customers"


def segment_mode(series: pd.Series) -> Any:
    values = series.dropna()
    if values.empty:
        return "Unknown"
    return values.mode().iloc[0]


def summarize_segments(customer_df: pd.DataFrame) -> pd.DataFrame:
    total_customers = customer_df["User_ID"].nunique()

    segment_summary = (
        customer_df.groupby("customer_segment")
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("monetary", "sum"),
            total_purchase_frequency=("frequency", "sum"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_total_spending=("monetary", "mean"),
            avg_rfm_score=("rfm_score", "mean"),
            avg_value_proxy_score=("value_proxy_score", "mean"),
            avg_recency_score=("recency_score", "mean"),
            avg_frequency_score=("frequency_score", "mean"),
            avg_monetary_score=("monetary_score", "mean"),
            category_preference=("category_preference", segment_mode),
        )
        .reset_index()
    )

    segment_summary["share_pct"] = (
        segment_summary["customer_count"] / total_customers * 100
    ).round(1)
    segment_summary["share"] = segment_summary["share_pct"].map(lambda value: f"{value:.1f}%")
    segment_summary["weighted_aov"] = segment_summary.apply(
        lambda row: safe_divide(row["total_spending"], row["total_purchase_frequency"]),
        axis=1,
    ).round(2)

    segment_summary["business_role"] = segment_summary["customer_segment"].map(ROLE_MAPPING)
    segment_summary["key_issue"] = segment_summary["customer_segment"].map(ISSUE_MAPPING)
    segment_summary["action_priority"] = segment_summary["customer_segment"].map(PRIORITY_MAPPING)

    segment_summary["frequency_range"] = segment_summary["avg_frequency"].round(2).astype(str)
    segment_summary["monetary_range"] = (
        "Avg total spending CNY "
        + segment_summary["avg_total_spending"].round(2).astype(str)
    )

    output = segment_summary.rename(columns={"customer_segment": "segment"})[
        [
            "segment",
            "share",
            "share_pct",
            "customer_count",
            "business_role",
            "frequency_range",
            "monetary_range",
            "weighted_aov",
            "avg_recency_days",
            "avg_rfm_score",
            "avg_value_proxy_score",
            "avg_recency_score",
            "avg_frequency_score",
            "avg_monetary_score",
            "category_preference",
            "key_issue",
            "action_priority",
        ]
    ]

    output["segment"] = pd.Categorical(output["segment"], categories=SEGMENT_ORDER, ordered=True)
    output = output.sort_values("segment").reset_index(drop=True)

    rounded_columns = [
        "avg_recency_days",
        "avg_rfm_score",
        "avg_value_proxy_score",
        "avg_recency_score",
        "avg_frequency_score",
        "avg_monetary_score",
    ]
    output[rounded_columns] = output[rounded_columns].round(2)

    return output


def build_fact_user_behavior_scored(customer_df: pd.DataFrame) -> pd.DataFrame:
    """Build the Power BI fact table used by main visuals and segment counts."""

    fact = customer_df.copy()
    fact["segment_name"] = fact["customer_segment"]
    fact["segment_name_cn"] = fact["segment_name"].map(SEGMENT_CN_MAPPING)
    fact["business_role"] = fact["segment_name"].map(ROLE_MAPPING)
    fact["action_priority"] = fact["segment_name"].map(PRIORITY_MAPPING)

    fact = fact.rename(
        columns={
            "age": "Age",
            "gender": "Gender",
            "location": "Location",
            "income": "Income",
            "interests": "Interests",
            "recency_days": "Last_Login_Days_Ago",
            "frequency": "Purchase_Frequency",
            "average_order_value": "Average_Order_Value",
            "monetary": "Total_Spending",
            "category_preference": "Product_Category_Preference",
            "time_spent_minutes": "Time_Spent_on_Site_Minutes",
            "pages_viewed": "Pages_Viewed",
            "newsletter_subscription": "Newsletter_Subscription",
            "recency_score": "r_score",
            "frequency_score": "f_score",
            "monetary_score": "m_score",
        }
    )

    output_columns = [
        "User_ID",
        "Age",
        "Gender",
        "Location",
        "Income",
        "Interests",
        "Last_Login_Days_Ago",
        "Purchase_Frequency",
        "Average_Order_Value",
        "Total_Spending",
        "Product_Category_Preference",
        "Time_Spent_on_Site_Minutes",
        "Pages_Viewed",
        "Newsletter_Subscription",
        "weighted_aov",
        "r_score",
        "f_score",
        "m_score",
        "rfm_score",
        "value_proxy_score",
        "segment_name",
        "segment_name_cn",
        "business_role",
        "action_priority",
    ]

    fact = fact[output_columns].copy()
    rounded_columns = [
        "Age",
        "Income",
        "Average_Order_Value",
        "Total_Spending",
        "weighted_aov",
        "value_proxy_score",
    ]
    fact[rounded_columns] = fact[rounded_columns].round(2)
    fact["rfm_score"] = fact["rfm_score"].astype(int)

    return fact


def filtered_or_full(df: pd.DataFrame, minimum_count: int) -> pd.DataFrame:
    filtered = df[df["customer_count"] >= minimum_count].copy()
    if filtered.empty:
        return df.copy()
    return filtered


def build_cross_dimensional_insights(customer_df: pd.DataFrame) -> pd.DataFrame:
    age_gender = (
        customer_df.groupby(["age", "gender"])
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("monetary", "sum"),
            total_purchase_frequency=("frequency", "sum"),
        )
        .reset_index()
    )
    age_gender["weighted_aov"] = age_gender.apply(
        lambda row: safe_divide(row["total_spending"], row["total_purchase_frequency"]),
        axis=1,
    )
    age_gender_valid = filtered_or_full(age_gender, minimum_count=5)
    elite_row = age_gender_valid.sort_values(
        ["weighted_aov", "customer_count"],
        ascending=False,
    ).iloc[0]

    region_category = (
        customer_df.groupby(["location", "category_preference"])
        .agg(
            customer_count=("User_ID", "nunique"),
            total_spending=("monetary", "sum"),
            total_purchase_frequency=("frequency", "sum"),
        )
        .reset_index()
    )
    region_category["weighted_aov"] = region_category.apply(
        lambda row: safe_divide(row["total_spending"], row["total_purchase_frequency"]),
        axis=1,
    )
    region_category_valid = filtered_or_full(region_category, minimum_count=10)
    best_region_category = region_category_valid.sort_values(
        ["weighted_aov", "customer_count"],
        ascending=False,
    ).iloc[0]

    user_value = customer_df[["User_ID", "monetary"]].sort_values("monetary", ascending=False)
    top_10_count = max(1, int(len(user_value) * 0.1))
    top_10_spending = user_value.head(top_10_count)["monetary"].sum()
    total_spending = user_value["monetary"].sum()
    top_10_share = round(safe_divide(top_10_spending, total_spending) * 100, 1)

    churn_users = customer_df[customer_df["customer_segment"] == "Churn-risk Customers"]
    churn_share = round(safe_divide(len(churn_users), len(customer_df)) * 100, 1)
    churn_top_category = segment_mode(churn_users["category_preference"]) if not churn_users.empty else "N/A"

    high_value_users = customer_df[customer_df["customer_segment"] == "High-value Customers"]
    high_value_top_category = (
        segment_mode(high_value_users["category_preference"]) if not high_value_users.empty else "N/A"
    )

    rows = [
        {
            "insight_name": "Elite Customer Segment",
            "dimension": "Age + Gender + Weighted AOV",
            "key_finding": (
                f"{elite_row['gender']} customers around age {int(round(elite_row['age']))} "
                f"show the highest weighted AOV ({elite_row['weighted_aov']:.2f}) among sufficiently sized groups."
            ),
            "business_meaning": "This group should be treated as a priority profit-driving segment.",
            "recommended_action": "Design premium product campaigns, expert review content, and VIP service benefits for this segment.",
        },
        {
            "insight_name": "Regional Category Opportunity",
            "dimension": "Location + Product Category + Weighted AOV",
            "key_finding": (
                f"{best_region_category['location']} customers in the "
                f"{best_region_category['category_preference']} category show strong weighted AOV "
                f"({best_region_category['weighted_aov']:.2f})."
            ),
            "business_meaning": "Regional category preference can reveal underexplored market opportunities.",
            "recommended_action": "Create region-specific product bundles and content campaigns based on category preference.",
        },
        {
            "insight_name": "Pareto Value Concentration",
            "dimension": "Customer Value Contribution",
            "key_finding": f"The top 10% users contribute approximately {top_10_share}% of total spending.",
            "business_meaning": "Revenue is concentrated among higher-value customers.",
            "recommended_action": "Prioritize retention and service resources for top-value users.",
        },
        {
            "insight_name": "Churn Recovery",
            "dimension": "Recency + Monetary + Category Preference",
            "key_finding": (
                f"{churn_share}% of users are high-spending but inactive, "
                f"with strongest preference in {churn_top_category}."
            ),
            "business_meaning": "These users should be treated as dormant premium assets rather than low-value inactive users.",
            "recommended_action": "Build win-back campaigns with product upgrade reminders, after-sales recovery, and service follow-up.",
        },
        {
            "insight_name": "High-value Category Focus",
            "dimension": "Segment + Product Category",
            "key_finding": f"High-value customers show the strongest preference in {high_value_top_category}.",
            "business_meaning": "Category preference helps translate high-value segmentation into campaign themes.",
            "recommended_action": "Use category-specific VIP bundles and loyalty benefits for high-value customers.",
        },
    ]

    return pd.DataFrame(rows)


def record_for_segment(segments: pd.DataFrame, segment: str) -> dict[str, Any]:
    matched = segments[segments["segment"].astype(str).eq(segment)]
    if matched.empty:
        return {}
    return matched.iloc[0].to_dict()


def build_structured_summary(
    processed: ProcessedDataResult,
    run_time_utc: str | None = None,
) -> dict[str, Any]:
    run_time = run_time_utc or utc_now_iso()
    segments = processed.customer_segments
    insights = processed.cross_dimensional_insights

    total_spending = round(float(processed.customer_level_data["monetary"].sum()), 2)
    total_frequency = round(float(processed.customer_level_data["frequency"].sum()), 2)

    summary = {
        "run_time_utc": run_time,
        "data_sources": [stat.to_metadata() for stat in processed.raw_files],
        "raw_row_count": processed.raw_row_count,
        "cleaned_row_count": processed.cleaned_row_count,
        "processed_customer_count": processed.processed_customer_count,
        "metrics_definition": {
            "recency": "Last_Login_Days_Ago; lower means more recent activity.",
            "frequency": "Purchase_Frequency aggregated per customer.",
            "monetary": "Total_Spending aggregated per customer.",
            "weighted_aov": "Total spending divided by total purchase frequency.",
            "value_proxy_score": "0-100 percentile score: 45% monetary, 25% frequency, 20% weighted AOV, 10% recency.",
            "rfm_score": "Recency, frequency, and monetary scores on a 1-5 scale; higher is better.",
        },
        "overall_metrics": {
            "total_spending": total_spending,
            "total_purchase_frequency": total_frequency,
            "overall_weighted_aov": round(safe_divide(total_spending, total_frequency), 2),
        },
        "segment_results": segments.to_dict(orient="records"),
        "key_segments": {
            "high_value": record_for_segment(segments, "High-value Customers"),
            "churn_risk": record_for_segment(segments, "Churn-risk Customers"),
            "potential": record_for_segment(segments, "Potential Customers"),
        },
        "cross_dimensional_insights": insights.to_dict(orient="records"),
        "guardrails": [
            "All numerical claims must come from this structured summary.",
            "LLM output is a draft for human review and must not trigger customer-facing campaigns automatically.",
        ],
    }

    return summary


def run_processing(raw_dir: Path = RAW_DIR) -> ProcessedDataResult:
    raw_df, stats = load_raw_data(raw_dir)
    customer_level_data = build_customer_level_data(raw_df)
    fact_user_behavior_scored = build_fact_user_behavior_scored(customer_level_data)
    customer_segments = summarize_segments(customer_level_data)
    cross_dimensional_insights = build_cross_dimensional_insights(customer_level_data)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    fact_user_behavior_scored.to_csv(FACT_USER_BEHAVIOR_SCORED_FILE, index=False, encoding="utf-8-sig")
    customer_segments.to_csv(CUSTOMER_SEGMENTS_FILE, index=False, encoding="utf-8-sig")
    cross_dimensional_insights.to_csv(CROSS_INSIGHTS_FILE, index=False, encoding="utf-8-sig")

    return ProcessedDataResult(
        raw_files=stats,
        raw_row_count=sum(stat.row_count for stat in stats),
        cleaned_row_count=sum(stat.cleaned_row_count for stat in stats),
        processed_customer_count=customer_level_data["User_ID"].nunique(),
        customer_level_data=customer_level_data,
        fact_user_behavior_scored=fact_user_behavior_scored,
        customer_segments=customer_segments,
        cross_dimensional_insights=cross_dimensional_insights,
        output_files={
            "fact_user_behavior_scored": FACT_USER_BEHAVIOR_SCORED_FILE,
            "customer_segments": CUSTOMER_SEGMENTS_FILE,
            "cross_dimensional_insights": CROSS_INSIGHTS_FILE,
        },
    )


def main() -> None:
    print("Loading and cleaning raw e-commerce CSV files from data/raw...")
    processed = run_processing()
    print(f"Raw rows read: {processed.raw_row_count}")
    print(f"Cleaned rows used: {processed.cleaned_row_count}")
    print(f"Processed customers: {processed.processed_customer_count}")
    print(f"Saved: {FACT_USER_BEHAVIOR_SCORED_FILE}")
    print(f"Saved: {CUSTOMER_SEGMENTS_FILE}")
    print(f"Saved: {CROSS_INSIGHTS_FILE}")


if __name__ == "__main__":
    main()
